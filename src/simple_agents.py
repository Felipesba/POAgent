"""
Sistema simplificado de agentes para Python 3.9
Funciona sem CrewAI usando OpenAI diretamente
"""

import os
from typing import Dict, List, Any, Optional
from openai import OpenAI
from src.document_processor import DocumentProcessor
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

class SimpleAgent:
    """Agente base simplificado"""
    
    def __init__(self, name: str, role: str, expertise: str):
        self.name = name
        self.role = role
        self.expertise = expertise
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.model = os.getenv('OPENAI_MODEL_NAME', 'gpt-4-turbo-preview')
        self.document_processor = DocumentProcessor()
    
    def execute_task(self, task_description: str, context: str = None) -> str:
        """Executar uma task específica"""
        try:
            # Construir prompt com contexto
            system_prompt = f"""Você é um {self.role} especializado em {self.expertise}.
            
            Sua expertise inclui:
            - Mercado financeiro brasileiro
            - Regulamentação CVM, BACEN e AMBIMA
            - Sistemas de custódia de ativos
            - Compliance e governança
            - Tecnologia financeira
            
            Forneça respostas detalhadas, técnicas e baseadas em conhecimento especializado."""
            
            user_prompt = task_description
            if context:
                user_prompt += f"\n\nCONTEXTO ADICIONAL:\n{context}"
            
            # Buscar informações relevantes nos documentos
            relevant_docs = self.document_processor.get_document_context(task_description, 3000)
            if relevant_docs:
                user_prompt += f"\n\nINFORMAÇÕES DOS DOCUMENTOS INDEXADOS:\n{relevant_docs}"
            
            response = self.client.chat.completions.create(
                model=self.model,
                temperature=0.1,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Erro na execução do agente {self.name}: {str(e)}")
            raise


class DocumentIntelligenceAgent(SimpleAgent):
    """Agente especializado em análise de documentos"""
    
    def __init__(self):
        super().__init__(
            name="Document Intelligence Specialist",
            role="Especialista em Inteligência Documental",
            expertise="análise de documentos regulatórios brasileiros, extração de requisitos legais, interpretação de normas CVM/BACEN/AMBIMA"
        )
    
    def analyze_documents(self, query: str) -> str:
        """Analisar documentos para uma consulta específica"""
        task = f"""Analise os documentos indexados e extraia informações relevantes para: {query}

        FOQUE EM:
        1. Requisitos regulatórios obrigatórios
        2. Obrigações e responsabilidades
        3. Prazos e deadlines
        4. Penalidades por não conformidade
        5. Requisitos técnicos específicos
        
        FORMATE COMO:
        - Resumo executivo
        - Lista de requisitos identificados
        - Análise de riscos
        - Recomendações práticas
        - Referências dos documentos"""
        
        return self.execute_task(task)


class ProductStrategyAgent(SimpleAgent):
    """Agente especializado em estratégia de produto e PRDs"""
    
    def __init__(self):
        super().__init__(
            name="Product Strategy Director",
            role="Diretor de Estratégia de Produto",
            expertise="desenvolvimento de PRDs, análise de mercado financeiro, estratégia de produto para soluções de custódia"
        )
    
    def generate_prd(self, request: str, context: str = None) -> str:
        """Gerar PRD completo"""
        task = f"""Crie um PRD (Product Requirements Document) detalhado para: {request}

        O PRD DEVE INCLUIR:
        
        1. RESUMO EXECUTIVO
           - Visão e objetivos do produto
           - Value proposition
           - Success metrics (KPIs)
        
        2. CONTEXTO DE MERCADO
           - Landscape regulatório brasileiro
           - Oportunidade de mercado
           - Análise competitiva
        
        3. REQUIREMENTS FUNCIONAIS
           - User stories detalhadas
           - Acceptance criteria
           - Business rules
        
        4. REQUIREMENTS NÃO-FUNCIONAIS
           - Performance
           - Security
           - Scalability
           - Compliance
        
        5. INTEGRAÇÃO E TÉCNICO
           - Sistemas externos (B3, SELIC, CETIP)
           - Arquitetura de alto nível
           - Considerações de segurança
        
        6. ROADMAP DE IMPLEMENTAÇÃO
           - Fases de desenvolvimento
           - Milestones
           - Dependências
           - Risk assessment
        
        Use formato markdown estruturado."""
        
        return self.execute_task(task, context)


class FeatureEngineeringAgent(SimpleAgent):
    """Agente especializado em engenharia de features"""
    
    def __init__(self):
        super().__init__(
            name="Feature Engineering Specialist",
            role="Especialista em Engenharia de Features",
            expertise="especificações técnicas detalhadas, arquitetura de sistemas financeiros, APIs e integrações"
        )
    
    def generate_feature_specs(self, request: str, context: str = None) -> str:
        """Gerar especificações técnicas de features"""
        task = f"""Crie especificações técnicas detalhadas para: {request}

        ESPECIFICAÇÕES DEVEM INCLUIR:
        
        1. FEATURE OVERVIEW
           - Descrição funcional
           - Business value
           - Success criteria
           - Dependencies
        
        2. ESPECIFICAÇÃO TÉCNICA
           - Arquitetura de componentes
           - Data models e schemas
           - API endpoints e contracts
           - Security considerations
           - Performance requirements
        
        3. USER EXPERIENCE
           - User flows
           - Interface mockups conceituais
           - Error handling
           - Accessibility
        
        4. INTEGRAÇÃO
           - Sistemas externos
           - Protocolos de comunicação
           - Authentication/authorization
           - Monitoring
        
        5. COMPLIANCE E SEGURANÇA
           - Mapeamento regulatório
           - Controles de segurança
           - Audit trail
           - Risk mitigation
        
        6. TESTING
           - Unit testing
           - Integration testing
           - Performance testing
           - Security testing
        
        Use formato markdown estruturado com exemplos práticos."""
        
        return self.execute_task(task, context)


class SimpleCustodySystem:
    """Sistema principal simplificado para Python 3.9"""
    
    def __init__(self):
        self.doc_agent = DocumentIntelligenceAgent()
        self.product_agent = ProductStrategyAgent()
        self.feature_agent = FeatureEngineeringAgent()
        self.document_processor = DocumentProcessor()
        
        logger.info("SimpleCustodySystem inicializado com sucesso")
    
    def generate_prd(self, user_request: str, context: str = None) -> str:
        """Gerar PRD usando múltiplos agentes"""
        try:
            logger.info(f"Gerando PRD para: {user_request[:100]}...")
            
            # 1. Análise de documentos primeiro
            doc_analysis = self.doc_agent.analyze_documents(user_request)
            
            # 2. Gerar PRD com contexto da análise
            full_context = doc_analysis
            if context:
                full_context += f"\n\nCONTEXTO ADICIONAL:\n{context}"
            
            prd = self.product_agent.generate_prd(user_request, full_context)
            
            logger.info("PRD gerado com sucesso")
            return prd
            
        except Exception as e:
            logger.error(f"Erro na geração de PRD: {str(e)}")
            raise
    
    def generate_features(self, user_request: str, context: str = None) -> str:
        """Gerar especificações de features"""
        try:
            logger.info(f"Gerando features para: {user_request[:100]}...")
            
            # 1. Análise regulatória primeiro
            regulatory_analysis = self.doc_agent.analyze_documents(user_request)
            
            # 2. Gerar specs com contexto regulatório
            full_context = regulatory_analysis
            if context:
                full_context += f"\n\nCONTEXTO ADICIONAL:\n{context}"
            
            features = self.feature_agent.generate_feature_specs(user_request, full_context)
            
            logger.info("Features geradas com sucesso")
            return features
            
        except Exception as e:
            logger.error(f"Erro na geração de features: {str(e)}")
            raise
    
    def analyze_compliance(self, regulation_area: str) -> str:
        """Análise focada em compliance"""
        try:
            logger.info(f"Analisando compliance para: {regulation_area}")
            
            result = self.doc_agent.analyze_documents(
                f"Análise completa de compliance para {regulation_area}"
            )
            
            logger.info("Análise de compliance concluída")
            return result
            
        except Exception as e:
            logger.error(f"Erro na análise de compliance: {str(e)}")
            raise