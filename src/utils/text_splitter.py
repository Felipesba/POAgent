"""
Divisor de texto inteligente para processamento de documentos
"""

import re
import tiktoken
from typing import List, Optional

class CustomTextSplitter:
    def __init__(self, 
                 chunk_size: int = 1000, 
                 chunk_overlap: int = 200,
                 encoding_name: str = "cl100k_base"):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.encoding = tiktoken.get_encoding(encoding_name)
        
    def split_text(self, text: str) -> List[str]:
        """Dividir texto em chunks inteligentes"""
        if not text.strip():
            return []
        
        # Limpar texto
        text = self._clean_text(text)
        
        # Dividir por seções maiores primeiro
        sections = self._split_by_sections(text)
        
        chunks = []
        for section in sections:
            # Se a seção é pequena, adicionar diretamente
            if self._count_tokens(section) <= self.chunk_size:
                if section.strip():
                    chunks.append(section.strip())
            else:
                # Dividir seção grande em chunks menores
                section_chunks = self._split_section(section)
                chunks.extend(section_chunks)
        
        return chunks
    
    def _clean_text(self, text: str) -> str:
        """Limpar e normalizar texto"""
        # Remover linhas em branco excessivas
        text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
        
        # Normalizar espaços
        text = re.sub(r' +', ' ', text)
        
        # Remover caracteres de controle
        text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', text)
        
        return text.strip()
    
    def _split_by_sections(self, text: str) -> List[str]:
        """Dividir texto por seções lógicas"""
        # Padrões para identificar seções
        section_patterns = [
            r'\n(?=CAPÍTULO|SEÇÃO|ARTIGO|Art\.|Artigo)',  # Documentos legais
            r'\n(?=\d+\.\s)',  # Listas numeradas
            r'\n(?=[A-Z][A-Z\s]{10,})',  # Títulos em maiúsculas
            r'\n\n(?=\w)',  # Parágrafos
        ]
        
        sections = [text]
        
        for pattern in section_patterns:
            new_sections = []
            for section in sections:
                parts = re.split(pattern, section)
                if len(parts) > 1:
                    # Manter o delimitador com a seção seguinte
                    new_sections.append(parts[0])
                    for i in range(1, len(parts)):
                        new_sections.append(parts[i])
                else:
                    new_sections.append(section)
            sections = new_sections
        
        return [s for s in sections if s.strip()]
    
    def _split_section(self, section: str) -> List[str]:
        """Dividir seção em chunks menores"""
        if self._count_tokens(section) <= self.chunk_size:
            return [section.strip()] if section.strip() else []
        
        # Dividir por sentenças
        sentences = self._split_by_sentences(section)
        
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            # Calcular tokens se adicionarmos esta sentença
            potential_chunk = current_chunk + " " + sentence if current_chunk else sentence
            
            if self._count_tokens(potential_chunk) <= self.chunk_size:
                current_chunk = potential_chunk
            else:
                # Adicionar chunk atual se não estiver vazio
                if current_chunk:
                    chunks.append(current_chunk.strip())
                
                # Verificar se a sentença única é muito grande
                if self._count_tokens(sentence) > self.chunk_size:
                    # Dividir sentença por força bruta
                    sub_chunks = self._force_split(sentence)
                    chunks.extend(sub_chunks)
                    current_chunk = ""
                else:
                    current_chunk = sentence
        
        # Adicionar último chunk
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        # Aplicar overlap
        return self._apply_overlap(chunks)
    
    def _split_by_sentences(self, text: str) -> List[str]:
        """Dividir texto por sentenças"""
        # Padrão para final de sentença
        sentence_pattern = r'(?<=[.!?])\s+(?=[A-Z])'
        sentences = re.split(sentence_pattern, text)
        
        return [s.strip() for s in sentences if s.strip()]
    
    def _force_split(self, text: str) -> List[str]:
        """Divisão forçada por tokens quando necessário"""
        words = text.split()
        chunks = []
        current_chunk = ""
        
        for word in words:
            potential_chunk = current_chunk + " " + word if current_chunk else word
            
            if self._count_tokens(potential_chunk) <= self.chunk_size:
                current_chunk = potential_chunk
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = word
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def _apply_overlap(self, chunks: List[str]) -> List[str]:
        """Aplicar overlap entre chunks"""
        if len(chunks) <= 1 or self.chunk_overlap <= 0:
            return chunks
        
        overlapped_chunks = []
        
        for i, chunk in enumerate(chunks):
            if i == 0:
                overlapped_chunks.append(chunk)
            else:
                # Pegar últimas palavras do chunk anterior
                prev_chunk = chunks[i-1]
                prev_words = prev_chunk.split()
                
                # Calcular quantas palavras usar para overlap
                overlap_words = []
                overlap_tokens = 0
                
                for word in reversed(prev_words):
                    potential_overlap = [word] + overlap_words
                    potential_tokens = self._count_tokens(" ".join(potential_overlap))
                    
                    if potential_tokens <= self.chunk_overlap:
                        overlap_words = potential_overlap
                        overlap_tokens = potential_tokens
                    else:
                        break
                
                if overlap_words:
                    overlapped_chunk = " ".join(overlap_words) + " " + chunk
                    overlapped_chunks.append(overlapped_chunk)
                else:
                    overlapped_chunks.append(chunk)
        
        return overlapped_chunks
    
    def _count_tokens(self, text: str) -> int:
        """Contar tokens no texto"""
        try:
            return len(self.encoding.encode(text))
        except Exception:
            # Fallback: aproximar por palavras
            return len(text.split()) * 1.3