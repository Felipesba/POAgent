"""
Tasks específicas para análise de documentos e inteligência regulatória
"""

from crewai import Task
from typing import List

def create_document_analysis_task(agent, user_request: str, context: str = None) -> Task:
    """Criar task para análise de documentos"""
    
    context_section = f"\n\nCONTEXTO ADICIONAL:\n{context}" if context else ""
    
    return Task(
        description=f"""Analise os documentos indexados e extraia informações relevantes 
        para o seguinte pedido do usuário:

        PEDIDO: {user_request}
        {context_section}

        INSTRUÇÕES ESPECÍFICAS:
        1. Use a ferramenta document_search para buscar informações relevantes
        2. Use a ferramenta regulation_analyzer para análise regulatória detalhada
        3. Identifique requisitos legais e obrigatórios
        4. Extraia informações sobre:
           - Obrigações e responsabilidades
           - Prazos e deadlines
           - Penalidades por não conformidade
           - Requisitos técnicos específicos
           - Fluxos operacionais obrigatórios

        FOCO EM:
        - Regulamentação CVM (Comissão de Valores Mobiliários)
        - Normas BACEN (Banco Central do Brasil)
        - Diretrizes AMBIMA
        - Legislação sobre custódia de ativos
        - Compliance e governança

        FORMATO DE SAÍDA:
        Forneça um relatório estruturado com:
        - Resumo executivo das principais descobertas
        - Requisitos regulatórios identificados
        - Riscos e implicações de compliance
        - Recomendações para implementação
        - Referências aos documentos fonte""",
        agent=agent,
        expected_output="""Relatório estruturado de análise documental contendo:
        1. Resumo executivo (3-5 parágrafos)
        2. Requisitos regulatórios identificados (lista detalhada)
        3. Análise de riscos e compliance
        4. Recomendações práticas
        5. Referências e fontes utilizadas"""
    )


def create_regulatory_compliance_task(agent, specific_area: str) -> Task:
    """Criar task para análise de compliance regulatório"""
    
    return Task(
        description=f"""Realize uma análise aprofundada de compliance regulatório
        focada na área específica: {specific_area}

        OBJETIVO:
        Identificar todos os requisitos de compliance relacionados à área especificada
        e mapear as obrigações que um sistema de custódia deve atender.

        ANÁLISE DEVE INCLUIR:
        1. Mapeamento completo das obrigações regulatórias
        2. Identificação de prazos e deadlines críticos
        3. Análise de penalidades por não conformidade
        4. Requisitos de documentação e evidências
        5. Procedimentos obrigatórios e controles

        USE AS FERRAMENTAS:
        - regulation_analyzer: Para análise detalhada da regulamentação
        - document_search: Para buscar informações específicas
        - context_generator: Para gerar contexto abrangente

        ÁREAS DE FOCO:
        - Segregação patrimonial
        - Controles de risco
        - Relatórios obrigatórios
        - Auditoria e compliance
        - Integração com infraestrutura de mercado""",
        agent=agent,
        expected_output="""Análise completa de compliance contendo:
        1. Mapa de obrigações regulatórias
        2. Matriz de riscos de compliance
        3. Cronograma de obrigações (prazos)
        4. Lista de controles necessários
        5. Plano de evidenciação e documentação"""
    )


def create_knowledge_extraction_task(agent, documents_focus: List[str]) -> Task:
    """Criar task para extração de conhecimento específico"""
    
    focus_areas = ", ".join(documents_focus)
    
    return Task(
        description=f"""Extraia conhecimento especializado dos documentos indexados
        com foco nas seguintes áreas: {focus_areas}

        METODOLOGIA:
        1. Busque informações nos documentos usando termos técnicos específicos
        2. Identifique padrões e melhores práticas
        3. Extraia definições e conceitos importantes
        4. Mapeie processos e fluxos obrigatórios
        5. Identifique integrações necessárias

        EXTRAÇÃO DEVE COBRIR:
        - Definições técnicas e glossário
        - Processos operacionais detalhados
        - Requisitos de sistema e tecnologia
        - Interfaces e integrações obrigatórias
        - Métricas e indicadores de performance

        ESTRUTURE O CONHECIMENTO EM:
        - Conceitos fundamentais
        - Processos e workflows
        - Requisitos técnicos
        - Padrões e boas práticas
        - Casos de uso e exemplos""",
        agent=agent,
        expected_output="""Base de conhecimento estruturada contendo:
        1. Glossário de termos técnicos
        2. Mapa de processos operacionais
        3. Catálogo de requisitos técnicos
        4. Biblioteca de padrões e práticas
        5. Casos de uso documentados"""
    )