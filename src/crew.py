"""
Sistema principal CrewAI para geração de PRDs e Features de Custódia Brasileira
"""

from crewai import Crew, Process
from langchain_openai import ChatOpenAI
import os
from typing import Dict, Any, Optional

# Importar agentes
from src.agents.document_intelligence_agent import (
    
    create_document_intelligence_agent,
    create_document_analysis_specialist
)
from src.agents.product_strategy_agent import (
    create_product_strategy_agent,
    create_business_analyst_agent
)
from src.agents.feature_engineering_agent import (
    create_feature_engineering_agent,
    create_technical_architect_agent,
    create_qa_specialist_agent
)

# Importar tasks
from src.tasks.document_analysis_tasks import (
    create_document_analysis_task,
    create_regulatory_compliance_task,
    create_knowledge_extraction_task
)
from src.tasks.prd_generation_tasks import (
    create_prd_generation_task,
    create_business_analysis_task,
    create_market_research_task
)
from src.tasks.feature_engineering_tasks import (
    create_feature_specification_task,
    create_architecture_design_task,
    create_api_specification_task,
    create_database_design_task
)

# Importar tools
from src.tools.document_search_tool import DocumentSearchTool
from src.tools.context_generator_tool import ContextGeneratorTool
from src.tools.regulation_analyzer_tool import RegulationAnalyzerTool

from src.utils.logger import setup_logger

logger = setup_logger(__name__)

class CustodyPRDCrew:
    """Crew principal para geração de PRDs e Features de Custódia"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model=os.getenv('OPENAI_MODEL_NAME', 'gpt-4-turbo-preview'),
            temperature=0.1
        )
        
        # Inicializar tools compartilhadas
        self.tools = [
            DocumentSearchTool(),
            ContextGeneratorTool(),
            RegulationAnalyzerTool()
        ]
        
        # Inicializar agentes
        self._setup_agents()
        
        logger.info("CustodyPRDCrew inicializada com sucesso")
    
    def _setup_agents(self):
        """Configurar todos os agentes com suas tools"""
        
        # Document Intelligence Agents
        self.doc_intelligence_agent = create_document_intelligence_agent()
        self.doc_intelligence_agent.tools = self.tools
        
        self.doc_analysis_specialist = create_document_analysis_specialist()
        self.doc_analysis_specialist.tools = self.tools
        
        # Product Strategy Agents
        self.product_strategy_agent = create_product_strategy_agent()
        self.product_strategy_agent.tools = self.tools
        
        self.business_analyst_agent = create_business_analyst_agent()
        self.business_analyst_agent.tools = self.tools
        
        # Feature Engineering Agents
        self.feature_engineering_agent = create_feature_engineering_agent()
        self.feature_engineering_agent.tools = self.tools
        
        self.technical_architect_agent = create_technical_architect_agent()
        self.technical_architect_agent.tools = self.tools
        
        self.qa_specialist_agent = create_qa_specialist_agent()
        self.qa_specialist_agent.tools = self.tools
    
    def generate_prd(self, user_request: str, context: str = None) -> str:
        """Gerar PRD completo baseado no pedido do usuário"""
        
        try:
            logger.info(f"Iniciando geração de PRD para: {user_request[:100]}...")
            
            # Definir tasks para geração de PRD
            tasks = [
                # 1. Análise de documentos e regulamentação
                create_document_analysis_task(
                    agent=self.doc_intelligence_agent,
                    user_request=user_request,
                    context=context
                ),
                
                # 2. Análise de negócio
                create_business_analysis_task(
                    agent=self.business_analyst_agent,
                    business_context=user_request
                ),
                
                # 3. Pesquisa de mercado
                create_market_research_task(
                    agent=self.product_strategy_agent,
                    product_area=user_request
                ),
                
                # 4. Geração final do PRD
                create_prd_generation_task(
                    agent=self.product_strategy_agent,
                    user_request=user_request,
                    context=context
                )
            ]
            
            # Criar e executar crew
            crew = Crew(
                agents=[
                    self.doc_intelligence_agent,
                    self.business_analyst_agent,
                    self.product_strategy_agent
                ],
                tasks=tasks,
                process=Process.sequential,
                verbose=True
            )
            
            result = crew.kickoff()
            
            logger.info("PRD gerado com sucesso")
            return result
            
        except Exception as e:
            logger.error(f"Erro na geração de PRD: {str(e)}")
            raise
    
    def generate_features(self, user_request: str, context: str = None) -> str:
        """Gerar especificações detalhadas de features"""
        
        try:
            logger.info(f"Iniciando geração de features para: {user_request[:100]}...")
            
            # Definir tasks para geração de features
            tasks = [
                # 1. Análise regulatória e compliance
                create_regulatory_compliance_task(
                    agent=self.doc_analysis_specialist,
                    specific_area=user_request
                ),
                
                # 2. Especificação da feature
                create_feature_specification_task(
                    agent=self.feature_engineering_agent,
                    feature_request=user_request,
                    context=context
                ),
                
                # 3. Design de arquitetura
                create_architecture_design_task(
                    agent=self.technical_architect_agent,
                    system_component=user_request
                ),
                
                # 4. Especificação de APIs (se aplicável)
                create_api_specification_task(
                    agent=self.feature_engineering_agent,
                    api_purpose=user_request
                ),
                
                # 5. Estratégia de QA
                create_database_design_task(
                    agent=self.qa_specialist_agent,
                    data_domain=user_request
                )
            ]
            
            # Criar e executar crew
            crew = Crew(
                agents=[
                    self.doc_analysis_specialist,
                    self.feature_engineering_agent,
                    self.technical_architect_agent,
                    self.qa_specialist_agent
                ],
                tasks=tasks,
                process=Process.sequential,
                verbose=True
            )
            
            result = crew.kickoff()
            
            logger.info("Features geradas com sucesso")
            return result
            
        except Exception as e:
            logger.error(f"Erro na geração de features: {str(e)}")
            raise
    
    def analyze_compliance(self, regulation_area: str) -> str:
        """Análise focada em compliance regulatório"""
        
        try:
            logger.info(f"Iniciando análise de compliance para: {regulation_area}")
            
            tasks = [
                create_regulatory_compliance_task(
                    agent=self.doc_analysis_specialist,
                    specific_area=regulation_area
                ),
                
                create_knowledge_extraction_task(
                    agent=self.doc_intelligence_agent,
                    documents_focus=[regulation_area, "compliance", "auditoria"]
                )
            ]
            
            crew = Crew(
                agents=[
                    self.doc_analysis_specialist,
                    self.doc_intelligence_agent
                ],
                tasks=tasks,
                process=Process.sequential,
                verbose=True
            )
            
            result = crew.kickoff()
            
            logger.info("Análise de compliance concluída")
            return result
            
        except Exception as e:
            logger.error(f"Erro na análise de compliance: {str(e)}")
            raise
    
    def custom_analysis(self, 
                       request: str, 
                       agents_to_use: list = None, 
                       focus_areas: list = None) -> str:
        """Análise customizada com agentes específicos"""
        
        try:
            logger.info(f"Iniciando análise customizada: {request[:100]}...")
            
            # Determinar agentes a usar
            if not agents_to_use:
                agents_to_use = ['document_intelligence', 'product_strategy', 'feature_engineering']
            
            selected_agents = []
            tasks = []
            
            # Mapear agentes selecionados
            agent_mapping = {
                'document_intelligence': self.doc_intelligence_agent,
                'document_analysis': self.doc_analysis_specialist,
                'product_strategy': self.product_strategy_agent,
                'business_analyst': self.business_analyst_agent,
                'feature_engineering': self.feature_engineering_agent,
                'technical_architect': self.technical_architect_agent,
                'qa_specialist': self.qa_specialist_agent
            }
            
            for agent_key in agents_to_use:
                if agent_key in agent_mapping:
                    selected_agents.append(agent_mapping[agent_key])
            
            # Criar tasks baseadas nos agentes selecionados
            if 'document_intelligence' in agents_to_use or 'document_analysis' in agents_to_use:
                tasks.append(create_document_analysis_task(
                    agent=selected_agents[0],
                    user_request=request
                ))
            
            if 'product_strategy' in agents_to_use or 'business_analyst' in agents_to_use:
                tasks.append(create_business_analysis_task(
                    agent=agent_mapping.get('product_strategy', selected_agents[0]),
                    business_context=request
                ))
            
            if 'feature_engineering' in agents_to_use or 'technical_architect' in agents_to_use:
                tasks.append(create_feature_specification_task(
                    agent=agent_mapping.get('feature_engineering', selected_agents[0]),
                    feature_request=request
                ))
            
            # Executar crew customizada
            crew = Crew(
                agents=selected_agents,
                tasks=tasks,
                process=Process.sequential,
                verbose=True
            )
            
            result = crew.kickoff()
            
            logger.info("Análise customizada concluída")
            return result
            
        except Exception as e:
            logger.error(f"Erro na análise customizada: {str(e)}")
            raise
    
    def get_available_agents(self) -> Dict[str, str]:
        """Retornar lista de agentes disponíveis"""
        return {
            'document_intelligence': 'Document Intelligence Specialist',
            'document_analysis': 'Regulatory Document Analyst',
            'product_strategy': 'Product Strategy Director',
            'business_analyst': 'Senior Business Analyst',
            'feature_engineering': 'Senior Feature Engineering Specialist',
            'technical_architect': 'Solutions Architect',
            'qa_specialist': 'QA Engineering Specialist'
        }