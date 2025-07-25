"""
Tool para gerar contexto relevante baseado em consultas
"""

from crewai_tools import BaseTool
from typing import Type, Any
from pydantic import BaseModel, Field
from src.document_processor import DocumentProcessor
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

class ContextGeneratorInput(BaseModel):
    """Input para geração de contexto"""
    topic: str = Field(..., description="Tópico ou área de foco para geração de contexto")
    max_tokens: int = Field(default=4000, description="Limite máximo de tokens para o contexto")

class ContextGeneratorTool(BaseTool):
    name: str = "context_generator"
    description: str = """Ferramenta para gerar contexto relevante e estruturado sobre tópicos específicos
    baseado nos documentos indexados. Ideal para PRDs e especificações técnicas.
    
    Use esta ferramenta quando precisar de:
    - Contexto abrangente sobre um tópico específico
    - Informações consolidadas de múltiplos documentos
    - Base de conhecimento para decisões de produto
    
    Exemplos:
    - "regulamentação de custódia CVM"
    - "requisitos técnicos para integração B3"
    - "compliance BACEN para instituições financeiras"
    """
    args_schema: Type[BaseModel] = ContextGeneratorInput
    
    def _run(self, topic: str, max_tokens: int = 4000) -> str:
        try:
            processor = DocumentProcessor()
            context = processor.get_document_context(topic, max_tokens)
            
            if not context:
                return f"Nenhum contexto encontrado para o tópico: {topic}"
            
            # Estruturar contexto
            structured_context = f"""
CONTEXTO RELEVANTE: {topic.upper()}

{context}

---
NOTA: Este contexto foi gerado automaticamente a partir dos documentos indexados.
Verifique sempre as fontes originais para informações críticas.
"""
            
            logger.info(f"Contexto gerado para tópico: {topic}")
            return structured_context
            
        except Exception as e:
            logger.error(f"Erro na geração de contexto: {str(e)}")
            return f"Erro ao gerar contexto: {str(e)}"