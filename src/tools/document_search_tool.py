"""
Tool para busca semântica em documentos indexados
"""

from crewai_tools import BaseTool
from typing import Type, Any
from pydantic import BaseModel, Field
from src.document_processor import DocumentProcessor
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

class DocumentSearchInput(BaseModel):
    """Input para busca em documentos"""
    query: str = Field(..., description="Consulta para buscar nos documentos indexados")
    max_results: int = Field(default=10, description="Número máximo de resultados")

class DocumentSearchTool(BaseTool):
    name: str = "document_search"
    description: str = """Ferramenta para buscar informações em documentos indexados.
    Use esta ferramenta para encontrar informações específicas sobre regulamentação,
    requisitos legais, ou qualquer conteúdo dos documentos processados.
    
    Exemplos de uso:
    - "requisitos CVM para custódia de valores mobiliários"
    - "obrigações do custodiante segundo BACEN"
    - "procedimentos de liquidação AMBIMA"
    """
    args_schema: Type[BaseModel] = DocumentSearchInput
    
    def _run(self, query: str, max_results: int = 10) -> str:
        try:
            processor = DocumentProcessor()
            results = processor.search_documents(query, max_results)
            
            if not results:
                return "Nenhum documento relevante encontrado para a consulta."
            
            # Formatar resultados
            formatted_results = []
            for i, result in enumerate(results, 1):
                content = result['content'][:500] + "..." if len(result['content']) > 500 else result['content']
                
                formatted_result = f"""
RESULTADO {i} (Score: {result['similarity_score']:.3f})
Fonte: {result['metadata']['filename']}
Tipo: {result['metadata']['type']}

Conteúdo:
{content}

---
"""
                formatted_results.append(formatted_result)
            
            return "\n".join(formatted_results)
            
        except Exception as e:
            logger.error(f"Erro na busca de documentos: {str(e)}")
            return f"Erro ao buscar documentos: {str(e)}"