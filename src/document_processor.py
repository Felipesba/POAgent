"""
Processador de documentos para indexação e busca semântica
Suporta PDFs, TXT e links externos
"""

import os
import requests
import fitz  # PyMuPDF
import pypdf
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import tiktoken
from src.utils.logger import setup_logger
from src.utils.text_splitter import CustomTextSplitter

logger = setup_logger(__name__)

class DocumentProcessor:
    def __init__(self):
        self.chroma_client = self._setup_chroma()
        self.embeddings_model = SentenceTransformer(
            os.getenv('EMBEDDINGS_MODEL', 'all-MiniLM-L6-v2')
        )
        self.text_splitter = CustomTextSplitter()
        self.collection_name = "custody_documents"
        self.collection = self._get_or_create_collection()
        
    def _setup_chroma(self) -> chromadb.Client:
        """Configurar cliente ChromaDB"""
        persist_directory = os.getenv('CHROMA_PERSIST_DIRECTORY', './data/chroma_db')
        os.makedirs(persist_directory, exist_ok=True)
        
        try:
            return chromadb.PersistentClient(
                path=persist_directory,
                settings=Settings(anonymized_telemetry=False)
            )
        except Exception as e:
            logger.warning(f"Erro ao criar PersistentClient, usando EphemeralClient: {str(e)}")
            return chromadb.EphemeralClient()
    
    def _get_or_create_collection(self):
        """Obter ou criar coleção no ChromaDB"""
        try:
            return self.chroma_client.get_collection(self.collection_name)
        except Exception:
            return self.chroma_client.create_collection(
                name=self.collection_name,
                metadata={"description": "Documentos de custódia brasileira"}
            )
    
    def process_document(self, file_path: str, file_type: str) -> Dict[str, Any]:
        """Processar documento baseado no tipo"""
        try:
            if file_type == 'pdf':
                return self._process_pdf(file_path)
            elif file_type == 'txt':
                return self._process_txt(file_path)
            elif file_type == 'url':
                return self._process_url(file_path)
            else:
                raise ValueError(f"Tipo de arquivo não suportado: {file_type}")
                
        except Exception as e:
            logger.error(f"Erro ao processar documento {file_path}: {str(e)}")
            raise
    
    def _process_pdf(self, file_path: str) -> Dict[str, Any]:
        """Processar arquivo PDF usando PyMuPDF e pypdf como fallback"""
        text_content = ""
        filename = os.path.basename(file_path)
        
        try:
            # Tentar com PyMuPDF primeiro (melhor para layout complexo)
            doc = fitz.open(file_path)
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text_content += f"\n--- Página {page_num + 1} ---\n"
                text_content += page.get_text()
            doc.close()
            logger.info(f"PDF processado com PyMuPDF: {filename}")
            
        except Exception as e:
            logger.warning(f"Erro com PyMuPDF, tentando pypdf: {str(e)}")
            # Fallback para pypdf
            try:
                with open(file_path, 'rb') as file:
                    pdf_reader = pypdf.PdfReader(file)
                    for page_num, page in enumerate(pdf_reader.pages):
                        text_content += f"\n--- Página {page_num + 1} ---\n"
                        text_content += page.extract_text()
                logger.info(f"PDF processado com pypdf: {filename}")
                
            except Exception as e2:
                logger.error(f"Erro com ambos processadores de PDF: {str(e2)}")
                raise
        
        return self._index_document(text_content, filename, 'pdf', file_path)
    
    def _process_txt(self, file_path: str) -> Dict[str, Any]:
        """Processar arquivo TXT"""
        filename = os.path.basename(file_path)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text_content = file.read()
        except UnicodeDecodeError:
            # Tentar com diferentes encodings
            encodings = ['latin1', 'cp1252', 'iso-8859-1']
            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding) as file:
                        text_content = file.read()
                    logger.info(f"Arquivo TXT lido com encoding {encoding}: {filename}")
                    break
                except UnicodeDecodeError:
                    continue
            else:
                raise ValueError("Não foi possível decodificar o arquivo TXT")
        
        return self._index_document(text_content, filename, 'txt', file_path)
    
    def _process_url(self, url: str) -> Dict[str, Any]:
        """Processar conteúdo de URL"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            # Extrair texto simples (pode ser melhorado com BeautifulSoup)
            text_content = response.text
            filename = urlparse(url).netloc + urlparse(url).path.replace('/', '_')
            
            logger.info(f"URL processada: {url}")
            return self._index_document(text_content, filename, 'url', url)
            
        except Exception as e:
            logger.error(f"Erro ao processar URL {url}: {str(e)}")
            raise
    
    def _index_document(self, text_content: str, filename: str, doc_type: str, source_path: str) -> Dict[str, Any]:
        """Indexar documento na base vetorial"""
        try:
            # Dividir texto em chunks
            chunks = self.text_splitter.split_text(text_content)
            
            if not chunks:
                raise ValueError("Nenhum conteúdo extraído do documento")
            
            # Gerar embeddings
            embeddings = self.embeddings_model.encode(chunks).tolist()
            
            # Preparar metadados
            metadatas = []
            ids = []
            for i, chunk in enumerate(chunks):
                chunk_id = f"{filename}_{doc_type}_{i}"
                ids.append(chunk_id)
                metadatas.append({
                    'filename': filename,
                    'type': doc_type,
                    'source_path': source_path,
                    'chunk_index': i,
                    'chunk_size': len(chunk)
                })
            
            # Adicionar à coleção
            self.collection.add(
                embeddings=embeddings,
                documents=chunks,
                metadatas=metadatas,
                ids=ids
            )
            
            logger.info(f"Documento indexado: {filename} ({len(chunks)} chunks)")
            
            return {
                'message': f'Documento {filename} processado e indexado com sucesso',
                'chunks_count': len(chunks),
                'filename': filename,
                'type': doc_type
            }
            
        except Exception as e:
            logger.error(f"Erro ao indexar documento {filename}: {str(e)}")
            raise
    
    def search_documents(self, query: str, n_results: int = 10) -> List[Dict[str, Any]]:
        """Buscar documentos relevantes usando similaridade semântica"""
        try:
            # Gerar embedding da query
            query_embedding = self.embeddings_model.encode([query]).tolist()
            
            # Buscar documentos similares
            results = self.collection.query(
                query_embeddings=query_embedding,
                n_results=n_results,
                include=['documents', 'metadatas', 'distances']
            )
            
            # Formatar resultados
            formatted_results = []
            for i, (doc, metadata, distance) in enumerate(zip(
                results['documents'][0],
                results['metadatas'][0], 
                results['distances'][0]
            )):
                formatted_results.append({
                    'content': doc,
                    'metadata': metadata,
                    'similarity_score': 1 - distance,  # Converter distância para score
                    'rank': i + 1
                })
            
            logger.info(f"Busca realizada: {len(formatted_results)} resultados para '{query[:50]}...'")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Erro na busca: {str(e)}")
            raise
    
    def list_indexed_documents(self) -> List[Dict[str, Any]]:
        """Listar documentos indexados"""
        try:
            # Obter todos os metadados
            results = self.collection.get(include=['metadatas'])
            
            # Agrupar por documento
            docs_info = {}
            for metadata in results['metadatas']:
                filename = metadata['filename']
                if filename not in docs_info:
                    docs_info[filename] = {
                        'filename': filename,
                        'type': metadata['type'],
                        'source_path': metadata['source_path'],
                        'chunks': 0
                    }
                docs_info[filename]['chunks'] += 1
            
            return list(docs_info.values())
            
        except Exception as e:
            logger.error(f"Erro ao listar documentos: {str(e)}")
            return []
    
    def setup_vector_database(self):
        """Configurar base de dados vetorial"""
        try:
            # Verificar se a coleção existe
            collections = self.chroma_client.list_collections()
            collection_names = [col.name for col in collections]
            
            if self.collection_name not in collection_names:
                self.collection = self.chroma_client.create_collection(
                    name=self.collection_name,
                    metadata={"description": "Documentos de custódia brasileira"}
                )
                logger.info("Base de dados vetorial criada com sucesso")
            else:
                logger.info("Base de dados vetorial já existe")
                
        except Exception as e:
            logger.error(f"Erro ao configurar base de dados: {str(e)}")
            raise
    
    def get_document_context(self, query: str, max_tokens: int = 4000) -> str:
        """Obter contexto relevante para uma query"""
        try:
            # Buscar documentos relevantes
            results = self.search_documents(query, n_results=20)
            
            # Montar contexto respeitando limite de tokens
            context_parts = []
            total_tokens = 0
            
            encoding = tiktoken.get_encoding("cl100k_base")
            
            for result in results:
                content = result['content']
                tokens = len(encoding.encode(content))
                
                if total_tokens + tokens <= max_tokens:
                    context_parts.append(f"[{result['metadata']['filename']}] {content}")
                    total_tokens += tokens
                else:
                    break
            
            context = "\n\n---\n\n".join(context_parts)
            logger.info(f"Contexto gerado: {len(context_parts)} chunks, {total_tokens} tokens")
            
            return context
            
        except Exception as e:
            logger.error(f"Erro ao gerar contexto: {str(e)}")
            return ""