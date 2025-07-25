"""
Tasks específicas para engenharia de features e especificações técnicas
"""

from crewai import Task

def create_feature_specification_task(agent, feature_request: str, context: str = None) -> Task:
    """Criar task para especificação detalhada de features"""
    
    context_section = f"\n\nCONTEXTO ADICIONAL:\n{context}" if context else ""
    
    return Task(
        description=f"""Crie especificações técnicas detalhadas para a seguinte feature:

        FEATURE REQUEST: {feature_request}
        {context_section}

        ESPECIFICAÇÕES DEVEM INCLUIR:

        1. FEATURE OVERVIEW
           - Descrição funcional detalhada
           - Business value e justificativa
           - Success criteria mensuráveis
           - Dependencies e prerequisites

        2. TECHNICAL SPECIFICATION
           - Arquitetura de componentes
           - Data models e schemas
           - API endpoints e contracts
           - Security considerations
           - Performance requirements

        3. USER EXPERIENCE
           - User flows detalhados
           - Interface mockups conceituais
           - Interaction patterns
           - Error handling scenarios
           - Accessibility requirements

        4. INTEGRATION REQUIREMENTS
           - External system integrations
           - Message formats e protocols
           - Authentication e authorization
           - Rate limiting e throttling
           - Monitoring e observability

        5. COMPLIANCE & SECURITY
           - Regulatory compliance mappings
           - Security controls necessários
           - Audit trail requirements
           - Data privacy considerations
           - Risk mitigation strategies

        6. TESTING STRATEGY
           - Unit testing requirements
           - Integration testing scenarios
           - Performance testing criteria
           - Security testing protocols
           - User acceptance testing

        USE AS FERRAMENTAS:
        - document_search: Para buscar requirements regulatórios
        - context_generator: Para contexto técnico
        - regulation_analyzer: Para compliance analysis""",
        agent=agent,
        expected_output="""Especificação técnica completa contendo:
        1. Feature overview com business justification
        2. Especificação técnica detalhada
        3. User experience design
        4. Requirements de integração
        5. Compliance e security mappings
        6. Estratégia de testing abrangente
        7. Implementation guidelines
        8. Risk assessment e mitigation"""
    )


def create_architecture_design_task(agent, system_component: str) -> Task:
    """Criar task para design de arquitetura"""
    
    return Task(
        description=f"""Projete a arquitetura técnica para o componente: {system_component}

        DESIGN DE ARQUITETURA DEVE INCLUIR:

        1. SYSTEM ARCHITECTURE
           - High-level architecture diagram
           - Component breakdown e responsibilities  
           - Communication patterns
           - Data flow diagrams
           - Deployment architecture

        2. TECHNOLOGY STACK
           - Programming languages e frameworks
           - Database technologies
           - Message queues e event streaming
           - Caching strategies
           - Monitoring e logging tools

        3. SCALABILITY DESIGN
           - Horizontal scaling strategies
           - Load balancing approaches
           - Database scaling patterns
           - Caching layers
           - Performance optimization

        4. SECURITY ARCHITECTURE
           - Authentication e authorization
           - Encryption strategies
           - Network security
           - Application security
           - Compliance controls

        5. INTEGRATION PATTERNS
           - API design patterns
           - Message formats e protocols
           - Error handling e retry mechanisms
           - Circuit breaker patterns
           - Saga patterns for distributed transactions

        6. OPERATIONAL CONSIDERATIONS
           - Deployment strategies
           - Monitoring e alerting
           - Backup e recovery
           - Disaster recovery
           - Capacity planning

        FOQUE EM:
        - Financial systems best practices
        - High availability e fault tolerance
        - Regulatory compliance requirements
        - Brazilian market integrations""",
        agent=agent,
        expected_output="""Design de arquitetura técnica contendo:
        1. System architecture overview
        2. Technology stack recommendations
        3. Scalability e performance design
        4. Security architecture detalhada
        5. Integration patterns e protocols
        6. Operational procedures
        7. Risk assessment técnico
        8. Implementation roadmap"""
    )


def create_api_specification_task(agent, api_purpose: str) -> Task:
    """Criar task para especificação de APIs"""
    
    return Task(
        description=f"""Crie especificações detalhadas para APIs relacionadas a: {api_purpose}

        ESPECIFICAÇÃO DE API DEVE INCLUIR:

        1. API OVERVIEW
           - Purpose e business context
           - Target consumers
           - SLA requirements
           - Usage patterns esperados

        2. ENDPOINT SPECIFICATION
           - Resource endpoints detalhados
           - HTTP methods e semantics
           - Request/response schemas
           - Query parameters e filtering
           - Pagination strategies

        3. DATA MODELS
           - Entity definitions
           - Relationship mappings
           - Validation rules
           - Data formats e standards
           - Versioning strategy

        4. AUTHENTICATION & AUTHORIZATION
           - Authentication methods
           - Authorization patterns
           - API key management
           - Rate limiting policies
           - Security headers

        5. ERROR HANDLING
           - Error response formats
           - HTTP status codes
           - Error categorization
           - Retry mechanisms
           - Circuit breaker patterns

        6. MONITORING & OBSERVABILITY
           - Logging requirements
           - Metrics collection
           - Tracing strategies
           - Health check endpoints
           - Performance monitoring

        CONSIDERE:
        - RESTful design principles
        - OpenAPI 3.0 specification
        - Brazilian financial standards
        - Integration com sistemas legados
        - Compliance requirements""",
        agent=agent,
        expected_output="""Especificação completa de API contendo:
        1. API overview e business context
        2. Endpoint specifications detalhadas
        3. Data models e schemas
        4. Authentication e authorization
        5. Error handling strategies
        6. Monitoring e observability
        7. OpenAPI specification
        8. Integration guidelines"""
    )


def create_database_design_task(agent, data_domain: str) -> Task:
    """Criar task para design de banco de dados"""
    
    return Task(
        description=f"""Projete a estrutura de banco de dados para o domínio: {data_domain}

        DATABASE DESIGN DEVE INCLUIR:

        1. CONCEPTUAL MODEL
           - Entity relationship diagram
           - Business rules identification
           - Data flow mapping
           - Constraint definitions
           - Relationship cardinalities

        2. LOGICAL MODEL
           - Table structures detalhadas
           - Column specifications
           - Primary e foreign keys
           - Indexes strategy
           - Partitioning approach

        3. PHYSICAL MODEL
           - Storage considerations
           - Performance optimization
           - Backup e recovery strategy
           - Archiving policies
           - Capacity planning

        4. DATA GOVERNANCE
           - Data quality rules
           - Master data management
           - Data lineage tracking
           - Retention policies
           - Privacy controls

        5. SECURITY & COMPLIANCE
           - Access control matrix
           - Encryption strategies
           - Audit trail design
           - Compliance mappings
           - Data masking requirements

        6. INTEGRATION DESIGN
           - ETL/ELT processes
           - Real-time data streaming
           - API data access patterns
           - Reporting requirements
           - Analytics capabilities

        CONSIDERE:
        - ACID compliance requirements
        - Financial data standards
        - Regulatory reporting needs
        - High availability requirements
        - Disaster recovery needs""",
        agent=agent,
        expected_output="""Design de banco de dados completo contendo:
        1. Conceptual data model
        2. Logical database schema
        3. Physical implementation design
        4. Data governance framework
        5. Security e compliance controls
        6. Integration architecture
        7. Performance optimization
        8. Operational procedures"""
    )