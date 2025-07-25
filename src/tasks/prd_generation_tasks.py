"""
Tasks específicas para geração de PRDs (Product Requirements Documents)
"""

from crewai import Task

def create_prd_generation_task(agent, user_request: str, context: str = None) -> Task:
    """Criar task para geração de PRD"""
    
    context_section = f"\n\nCONTEXTO ADICIONAL:\n{context}" if context else ""
    
    return Task(
        description=f"""Crie um PRD (Product Requirements Document) detalhado baseado no pedido:

        PEDIDO DO USUÁRIO: {user_request}
        {context_section}

        INSTRUÇÕES:
        1. Use context_generator para obter contexto regulatório relevante
        2. Use document_search para buscar informações específicas sobre o pedido
        3. Analise requisitos de negócio e traduza em especificações de produto

        O PRD DEVE INCLUIR:

        1. RESUMO EXECUTIVO
           - Vision e missão do produto
           - Objetivos de negócio
           - Success metrics (KPIs)

        2. CONTEXTO DE MERCADO
           - Landscape regulatório brasileiro
           - Análise competitiva
           - Oportunidade de mercado

        3. REQUIREMENTS
           - Functional requirements detalhados
           - Non-functional requirements
           - Regulatory compliance requirements
           - Integration requirements

        4. USER STORIES & ACCEPTANCE CRITERIA
           - Personas principais
           - User journeys
           - Acceptance criteria detalhados

        5. TECHNICAL CONSIDERATIONS
           - Arquitetura de alto nível
           - Integrações necessárias (B3, SELIC, CETIP)
           - Considerações de segurança
           - Compliance e auditoria

        6. IMPLEMENTATION ROADMAP
           - Fases de desenvolvimento
           - Dependencies e milestones
           - Resource requirements
           - Risk assessment

        FOQUE EM:
        - Compliance com regulamentação brasileira
        - Integração com infraestrutura existente
        - Scalability e performance
        - Security e auditability
        - User experience otimizada""",
        agent=agent,
        expected_output="""PRD completo e detalhado no formato markdown contendo:
        1. Resumo executivo com objetivos claros
        2. Contexto de mercado e regulatório
        3. Requisitos funcionais e não-funcionais detalhados
        4. User stories com acceptance criteria
        5. Considerações técnicas e arquiteturais
        6. Roadmap de implementação com timelines
        7. Métricas de sucesso e KPIs
        8. Análise de riscos e mitigation strategies"""
    )


def create_business_analysis_task(agent, business_context: str) -> Task:
    """Criar task para análise de negócio"""
    
    return Task(
        description=f"""Realize uma análise de negócio aprofundada para o contexto:
        {business_context}

        ANÁLISE DEVE COBRIR:

        1. BUSINESS CASE
           - Problem statement detalhado
           - Current state vs desired state
           - Value proposition
           - ROI projection

        2. STAKEHOLDER ANALYSIS
           - Identificação de stakeholders chave
           - Pain points e necessidades
           - Success criteria por stakeholder
           - Impact assessment

        3. PROCESS MAPPING
           - Mapeamento de processos As-Is
           - Identificação de gaps e inefficiencies
           - Processo To-Be proposto
           - Change management requirements

        4. REGULATORY IMPACT
           - Análise de compliance requirements
           - Risk assessment regulatório
           - Audit trail necessários
           - Reporting obligations

        5. COMPETITIVE ANALYSIS
           - Market positioning
           - Competitive advantages
           - Differentiation strategy
           - Market trends

        USE AS FERRAMENTAS:
        - document_search: Para pesquisar informações relevantes
        - regulation_analyzer: Para análise regulatória
        - context_generator: Para contexto de mercado""",
        agent=agent,
        expected_output="""Análise de negócio completa contendo:
        1. Business case detalhado com ROI
        2. Mapa de stakeholders e requirements
        3. Process mapping (As-Is e To-Be)
        4. Assessment de impacto regulatório
        5. Análise competitiva e posicionamento
        6. Recomendações estratégicas"""
    )


def create_market_research_task(agent, product_area: str) -> Task:
    """Criar task para pesquisa de mercado"""
    
    return Task(
        description=f"""Conduza uma pesquisa de mercado focada em: {product_area}

        PESQUISA DEVE INCLUIR:

        1. MARKET SIZING
           - Total addressable market (TAM)
           - Serviceable addressable market (SAM)
           - Market growth trends
           - Key market drivers

        2. REGULATORY LANDSCAPE
           - Current regulatory framework
           - Upcoming regulatory changes
           - Compliance requirements
           - Regulatory risks e opportunities

        3. CUSTOMER SEGMENTS
           - Target customer profiles
           - Customer needs e pain points
           - Buying behavior patterns
           - Decision-making process

        4. COMPETITIVE INTELLIGENCE
           - Key players identification
           - Product offerings comparison
           - Pricing strategies
           - Market share analysis

        5. TECHNOLOGY TRENDS
           - Emerging technologies
           - Industry standards
           - Integration capabilities
           - Innovation opportunities

        FONTES DE INFORMAÇÃO:
        - Documentos regulatórios indexados
        - Conhecimento especializado sobre mercado brasileiro
        - Best practices internacionais aplicáveis""",
        agent=agent,
        expected_output="""Relatório de pesquisa de mercado contendo:
        1. Market sizing e growth projections
        2. Análise do landscape regulatório
        3. Segmentação de clientes e personas
        4. Competitive intelligence detalhada
        5. Technology trends e opportunities
        6. Market entry recommendations"""
    )