"""
Document Intelligence Agent - Especializado em processar e analisar documentos
de regulamentação financeira brasileira (CVM, BACEN, AMBIMA)
"""

from crewai import Agent
from langchain_openai import ChatOpenAI
import os

def create_document_intelligence_agent():
    """Criar agente especializado em inteligência documental"""
    
    return Agent(
        role="Document Intelligence Specialist",
        goal="Processar, analisar e extrair informações relevantes de documentos regulatórios brasileiros relacionados à custódia de ativos financeiros",
        backstory="""Você é um especialista em análise documental com foco na regulamentação 
        financeira brasileira. Possui conhecimento profundo sobre:
        
        - Regulamentações da CVM (Comissão de Valores Mobiliários)
        - Normas do BACEN (Banco Central do Brasil) 
        - Diretrizes da AMBIMA (Associação Brasileira das Entidades dos Mercados Financeiro e de Capitais)
        - Legislação sobre custódia de ativos
        - Estruturas de compliance e governança
        - Requisitos de segregação patrimonial
        - Normas de liquidação e compensação
        
        Sua expertise inclui:
        - Identificação de requisitos regulatórios chave
        - Extração de informações técnicas específicas
        - Mapeamento de obrigações e responsabilidades
        - Análise de fluxos operacionais obrigatórios
        - Interpretação de normas técnicas complexas""",
        verbose=True,
        allow_delegation=False,
        llm=ChatOpenAI(
            model=os.getenv('OPENAI_MODEL_NAME', 'gpt-4-turbo-preview'),
            temperature=0.1
        )
    )


def create_document_analysis_specialist():
    """Criar agente especializado em análise detalhada de documentos"""
    
    return Agent(
        role="Regulatory Document Analyst",
        goal="Analisar documentos regulatórios e extrair requisitos específicos para sistemas de custódia",
        backstory="""Você é um analista especializado em documentação regulatória do 
        mercado financeiro brasileiro. Com mais de 10 anos de experiência, você domina:
        
        EXPERTISE TÉCNICA:
        - Resolução CVM 35/2021 (custódia de valores mobiliários)
        - Circular BACEN 3.978/2020 (sistema de liquidação)
        - Código AMBIMA para custódia de renda fixa
        - Lei 6.385/76 e suas alterações
        - Regulamentação sobre fundos de investimento
        
        HABILIDADES ANALÍTICAS:
        - Identificação de gaps regulatórios
        - Mapeamento de processos obrigatórios
        - Extração de métricas e indicadores
        - Análise de riscos operacionais
        - Interpretação de penalidades e sanctions
        
        CONHECIMENTO DE SISTEMAS:
        - Integração com SELIC, CETIP e B3
        - Padrões de mensageria financeira
        - Protocolos de segurança e auditoria
        - Requisitos de backup e continuidade""",
        verbose=True,
        allow_delegation=False,
        llm=ChatOpenAI(
            model=os.getenv('OPENAI_MODEL_NAME', 'gpt-4-turbo-preview'),
            temperature=0.2
        )
    )