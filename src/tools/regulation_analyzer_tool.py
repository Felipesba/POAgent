"""
Tool especializada para análise de regulamentação financeira brasileira
"""

from crewai_tools import BaseTool
from typing import Type, Any, List, Dict
from pydantic import BaseModel, Field
from src.document_processor import DocumentProcessor
from src.utils.logger import setup_logger
import re

logger = setup_logger(__name__)

class RegulationAnalyzerInput(BaseModel):
    """Input para análise de regulamentação"""
    regulation_topic: str = Field(..., description="Tópico específico da regulamentação a ser analisado")
    focus_areas: List[str] = Field(default=[], description="Áreas específicas de foco (opcional)")

class RegulationAnalyzerTool(BaseTool):
    name: str = "regulation_analyzer"
    description: str = """Ferramenta especializada para análise de regulamentação financeira brasileira.
    Extrai e estrutura informações sobre:
    - Obrigações e responsabilidades
    - Prazos e deadlines
    - Penalidades e sanctions
    - Requisitos técnicos e operacionais
    - Fluxos obrigatórios
    
    Ideal para:
    - Análise de compliance
    - Mapeamento de riscos regulatórios
    - Identificação de gaps de conformidade
    - Planejamento de implementação
    """
    args_schema: Type[BaseModel] = RegulationAnalyzerInput
    
    def _run(self, regulation_topic: str, focus_areas: List[str] = None) -> str:
        try:
            processor = DocumentProcessor()
            
            # Buscar documentos relevantes
            results = processor.search_documents(regulation_topic, 20)
            
            if not results:
                return f"Nenhuma regulamentação encontrada para: {regulation_topic}"
            
            # Analisar e estruturar informações
            analysis = self._analyze_regulation_content(results, focus_areas or [])
            
            return self._format_analysis(regulation_topic, analysis)
            
        except Exception as e:
            logger.error(f"Erro na análise de regulamentação: {str(e)}")
            return f"Erro ao analisar regulamentação: {str(e)}"
    
    def _analyze_regulation_content(self, results: List[Dict], focus_areas: List[str]) -> Dict:
        """Analisar conteúdo regulatório e extrair informações estruturadas"""
        
        analysis = {
            'obligations': [],
            'deadlines': [],
            'penalties': [],
            'technical_requirements': [],
            'key_articles': [],
            'focus_analysis': {}
        }
        
        for result in results:
            content = result['content']
            metadata = result['metadata']
            
            # Extrair obrigações (verbos imperativos)
            obligations = re.findall(r'(?:deve|deverá|é obrigatório|é necessário|obriga-se)[\s\w,.:;-]+[.!]', content, re.IGNORECASE)
            analysis['obligations'].extend([{
                'text': ob.strip(),
                'source': metadata['filename']
            } for ob in obligations[:3]])  # Limitar a 3 por documento
            
            # Extrair prazos
            deadlines = re.findall(r'(?:prazo de|até|no prazo máximo de|em até)\s+\d+\s+(?:dias|meses|anos)[\s\w,.:;-]*[.!]', content, re.IGNORECASE)
            analysis['deadlines'].extend([{
                'text': dl.strip(),
                'source': metadata['filename']
            } for dl in deadlines[:2]])
            
            # Extrair penalidades
            penalties = re.findall(r'(?:multa|penalidade|sanção|advertência)[\s\w,.:;-]+[.!]', content, re.IGNORECASE)
            analysis['penalties'].extend([{
                'text': pen.strip(),
                'source': metadata['filename']
            } for pen in penalties[:2]])
            
            # Extrair artigos importantes
            articles = re.findall(r'(?:Art\.|Artigo)\s+\d+[\s\w,.:;-]+[.!]', content)
            analysis['key_articles'].extend([{
                'text': art.strip(),
                'source': metadata['filename']
            } for art in articles[:2]])
            
            # Análise focada em áreas específicas
            for area in focus_areas:
                if area.lower() in content.lower():
                    if area not in analysis['focus_analysis']:
                        analysis['focus_analysis'][area] = []
                    
                    # Extrair parágrafos relevantes
                    sentences = content.split('.')
                    relevant_sentences = [s.strip() + '.' for s in sentences if area.lower() in s.lower()]
                    
                    analysis['focus_analysis'][area].extend([{
                        'text': sent,
                        'source': metadata['filename']
                    } for sent in relevant_sentences[:2]])
        
        return analysis
    
    def _format_analysis(self, topic: str, analysis: Dict) -> str:
        """Formatar análise em texto estruturado"""
        
        sections = [
            f"ANÁLISE REGULATÓRIA: {topic.upper()}",
            "=" * 50,
            ""
        ]
        
        # Obrigações
        if analysis['obligations']:
            sections.extend([
                "📋 OBRIGAÇÕES E RESPONSABILIDADES:",
                ""
            ])
            for i, obligation in enumerate(analysis['obligations'][:5], 1):
                sections.append(f"{i}. {obligation['text']}")
                sections.append(f"   Fonte: {obligation['source']}")
                sections.append("")
        
        # Prazos
        if analysis['deadlines']:
            sections.extend([
                "⏰ PRAZOS E DEADLINES:",
                ""
            ])
            for i, deadline in enumerate(analysis['deadlines'][:3], 1):
                sections.append(f"{i}. {deadline['text']}")
                sections.append(f"   Fonte: {deadline['source']}")
                sections.append("")
        
        # Penalidades
        if analysis['penalties']:
            sections.extend([
                "⚠️ PENALIDADES E SANÇÕES:",
                ""
            ])
            for i, penalty in enumerate(analysis['penalties'][:3], 1):
                sections.append(f"{i}. {penalty['text']}")
                sections.append(f"   Fonte: {penalty['source']}")
                sections.append("")
        
        # Artigos importantes
        if analysis['key_articles']:
            sections.extend([
                "📖 ARTIGOS IMPORTANTES:",
                ""
            ])
            for i, article in enumerate(analysis['key_articles'][:3], 1):
                sections.append(f"{i}. {article['text']}")
                sections.append(f"   Fonte: {article['source']}")
                sections.append("")
        
        # Análise focada
        if analysis['focus_analysis']:
            sections.extend([
                "🎯 ANÁLISE FOCADA:",
                ""
            ])
            for area, items in analysis['focus_analysis'].items():
                sections.append(f"► {area.upper()}:")
                for item in items[:2]:
                    sections.append(f"  • {item['text']}")
                    sections.append(f"    Fonte: {item['source']}")
                sections.append("")
        
        sections.extend([
            "---",
            "NOTA: Esta análise foi gerada automaticamente. Consulte sempre as fontes originais para decisões críticas."
        ])
        
        return "\n".join(sections)