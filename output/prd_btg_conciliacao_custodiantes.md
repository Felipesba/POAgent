# PRD - Sistema de Conciliação de Custodiantes Externos BTG

**Data**: 25/07/2025  
**Cliente**: BTG Pactual  
**Produto**: Sistema de Importação e Conciliação de Custodiantes Externos

---

## 1. RESUMO EXECUTIVO

### 1.1 Visão do Produto
Desenvolver um sistema integrado para importação, armazenamento e conciliação de dados de carteiras de fundos custodiados externamente, permitindo ao BTG identificar divergências entre valorações internas e externas de forma automatizada e precisa.

### 1.2 Objetivos de Negócio
- **Automatizar** o processo de importação de dados de custodiantes externos
- **Centralizar** informações de posições e movimentações em base única
- **Identificar** divergências de valoração de forma sistemática
- **Reduzir** risco operacional e tempo de reconciliação manual
- **Melhorar** controle e governança sobre ativos custodiados externamente

### 1.3 Success Metrics (KPIs)
- **Tempo de processamento**: Redução de 80% no tempo de conciliação
- **Acurácia**: 99.9% de precisão na identificação de divergências
- **Cobertura**: 100% dos custodiantes externos integrados
- **Disponibilidade**: 99.5% de uptime do sistema
- **Automação**: 95% dos processos automatizados

---

## 2. CONTEXTO DE MERCADO

### 2.1 Landscape Regulatório Brasileiro
- **AMBIMA**: Conformidade com Layout de Movimentação de Fundos
- **CVM**: Requisitos de custódia qualificada (Resolução 35/2021)
- **BACEN**: Padrões XML para intercâmbio de dados financeiros
- **B3**: Integração com sistemas de liquidação e custódia

### 2.2 Análise Competitiva
- **Diferencial**: Sistema próprio de conciliação multi-custodiante
- **Vantagem**: Integração nativa com sistemas BTG existentes
- **Posicionamento**: Solução white-label para mercado institucional

### 2.3 Oportunidade de Mercado
- **Segmento**: Gestoras de recursos com múltiplos custodiantes
- **Necessidade**: Reconciliação automatizada e controle de risco
- **ROI**: Redução significativa de custos operacionais

---

## 3. REQUIREMENTS FUNCIONAIS

### 3.1 Módulo de Integração com Custodiantes Externos

#### RF001 - Conectores Multi-Custodiante
- **Descrição**: Integração com principais custodiantes (Itaú, Bradesco, Santander, etc.)
- **Entrada**: XML, E-mail, SFTP, APIs REST
- **Processamento**: Parse automático de formatos diversos
- **Saída**: Dados normalizados em formato padrão

#### RF002 - Recepção de Dados
- **Posições**: Saldos, cotas, valores por produto/fundo
- **Movimentações**: Aplicações, resgates, transferências
- **Metadados**: Timestamps, identificadores únicos, checksums

#### RF003 - Validação de Dados
- **Integridade**: Verificação de checksums e assinaturas
- **Completude**: Validação de campos obrigatórios
- **Consistência**: Regras de negócio por custodiante

### 3.2 Módulo de Armazenamento e Normalização

#### RF004 - Base de Dados Transacional
- **Schema**: Baseado no padrão XML BACEN
- **Estrutura**: Tabelas normalizadas por produto/cliente
- **Histórico**: Versionamento de posições e movimentações
- **Auditoria**: Log completo de operações

#### RF005 - Normalização de Dados
- **Mapeamento**: De/Para entre formatos de custodiantes
- **Padronização**: Códigos ISIN, CNPJ, tipos de ativo
- **Enriquecimento**: Adição de metadados e classificações

### 3.3 Módulo de Conciliação e Análise

#### RF006 - Engine de Conciliação
- **Matching**: Algoritmo de correspondência por produto/data
- **Comparação**: Valorações internas vs. externas
- **Tolerâncias**: Configuração de faixas aceitáveis de divergência

#### RF007 - Identificação de Divergências
- **Classificação**: Por tipo (saldo, movimentação, valoração)
- **Categorização**: Por produto, cliente, custodiante
- **Priorização**: Criticidade baseada em valor e impacto

#### RF008 - Relatórios e Dashboard
- **Dashboards**: Visualização em tempo real de divergências
- **Relatórios**: Exportação para Excel, PDF
- **Alertas**: Notificações automáticas para exceções

---

## 4. USER STORIES & ACCEPTANCE CRITERIA

### 4.1 Personas Principais
- **Analista de Reconciliação**: Operador do dia-a-dia
- **Gerente de Risk**: Supervisor de divergências críticas
- **Auditor Interno**: Usuário de consulta e controle

### 4.2 User Stories

#### US001 - Importação Automatizada
**Como** Analista de Reconciliação  
**Eu quero** que o sistema importe automaticamente dados dos custodiantes  
**Para que** eu não precise fazer download manual de arquivos

**Acceptance Criteria:**
- Sistema processa arquivos XML recebidos por e-mail
- Conecta via SFTP em horários programados
- Valida integridade dos dados recebidos
- Notifica falhas na importação

#### US002 - Identificação de Divergências
**Como** Gerente de Risk  
**Eu quero** visualizar divergências críticas em dashboard  
**Para que** eu possa tomar ações corretivas rapidamente

**Acceptance Criteria:**
- Dashboard atualizado em tempo real
- Filtros por custodiante, produto, valor
- Drill-down até nível de operação
- Exportação de relatórios detalhados

#### US003 - Auditoria e Controle
**Como** Auditor Interno  
**Eu quero** rastrear histórico de conciliações  
**Para que** eu possa evidenciar controles para auditoria

**Acceptance Criteria:**
- Log completo de operações
- Trilha de auditoria imutável
- Relatórios de compliance
- Arquivo de evidências

---

## 5. TECHNICAL CONSIDERATIONS

### 5.1 Arquitetura de Alto Nível
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Custodiantes  │───▶│  Data Ingestion  │───▶│  Data Storage   │
│   Externos      │    │     Layer        │    │     Layer       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Dashboard &   │◀───│  Business Logic  │◀───│  Valoração BTG  │
│   Reporting     │    │     Layer        │    │    Systems      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### 5.2 Tecnologias Recomendadas
- **Backend**: .NET Core 6+ (C#)
- **Database**: SQL Server 2019+ com particionamento
- **Message Queue**: RabbitMQ ou Azure Service Bus
- **API**: REST com OpenAPI 3.0
- **Cache**: Redis para performance
- **Logging**: ELK Stack (Elasticsearch, Logstash, Kibana)

### 5.3 Integrações Necessárias

#### Custodiantes Externos
- **Itaú**: SFTP + XML padrão CVM
- **Bradesco**: API REST + JSON
- **Santander**: E-mail + anexos XML
- **Outros**: Conectores customizáveis

#### Sistemas BTG
- **Sistema de Valoração**: API para busca de cotas
- **Core Banking**: Integração para clientes/produtos
- **Risk Management**: APIs de tolerância e limites

### 5.4 Considerações de Segurança
- **Autenticação**: OAuth 2.0 + JWT
- **Autorização**: RBAC (Role-Based Access Control)
- **Criptografia**: TLS 1.3 para transit, AES-256 at rest
- **Auditoria**: Logs tamper-proof com assinatura digital
- **Compliance**: LGPD e regulamentações financeiras

### 5.5 Performance Requirements
- **Throughput**: 1M+ transações/hora
- **Latência**: < 2s para consultas dashboard
- **Conciliação**: Processamento em < 30min
- **Disponibilidade**: 99.5% (máx 3.6h downtime/mês)

---

## 6. IMPLEMENTATION ROADMAP

### 6.1 Fase 1 - MVP (3 meses)
**Objetivos**: Prova de conceito com 1 custodiante
- Setup da infraestrutura base
- Desenvolvimento do módulo de ingestão
- Base de dados transacional
- Interface básica de consulta

**Entregáveis**:
- ✅ Conector Itaú funcionando
- ✅ Base de dados implementada
- ✅ API básica de consulta
- ✅ Dashboard simples

### 6.2 Fase 2 - Expansão (2 meses)
**Objetivos**: Integração com 3 principais custodiantes
- Conectores Bradesco e Santander
- Engine de conciliação básica
- Relatórios de divergências

**Entregáveis**:
- ✅ 3 custodiantes integrados
- ✅ Conciliação automatizada
- ✅ Alertas de divergências
- ✅ Relatórios gerenciais

### 6.3 Fase 3 - Produção (2 meses)
**Objetivos**: Sistema completo e produtivo
- Todos os custodiantes integrados
- Dashboard avançado
- Automação completa
- Monitoramento e alertas

**Entregáveis**:
- ✅ Sistema 100% funcional
- ✅ Todos os custodiantes
- ✅ Dashboard executivo
- ✅ Documentação completa

### 6.4 Dependencies e Milestones

#### Dependências Críticas
- **Acesso aos ambientes** dos custodiantes externos
- **Especificações técnicas** de cada custodiante
- **Credenciais e certificados** para integração
- **Ambiente de homologação** BTG

#### Milestones Principais
- **M1**: Primeiro conector funcionando (mês 1)
- **M2**: Base de dados e API prontas (mês 2)
- **M3**: Conciliação básica (mês 3)
- **M4**: Dashboard operacional (mês 5)
- **M5**: Go-live produção (mês 7)

---

## 7. RISK ASSESSMENT

### 7.1 Riscos Técnicos
| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| Latência de custodiantes | Alta | Médio | Cache + retry policies |
| Mudanças em APIs externas | Média | Alto | Versionamento + adapters |
| Volume de dados | Média | Alto | Particionamento + scaling |
| Disponibilidade | Baixa | Crítico | Redundância + DR |

### 7.2 Riscos de Negócio
| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| Resistência usuários | Média | Médio | Change management |
| Complexidade regulatória | Alta | Alto | Expertise jurídica |
| Custos operacionais | Media | Médio | ROI tracking |
| Integrações complexas | Alta | Alto | POCs antecipadas |

### 7.3 Riscos Operacionais
- **Falhas de integração**: Monitoramento 24/7 + alertas
- **Erro de conciliação**: Validação dupla + aprovação manual
- **Perda de dados**: Backup contínuo + replicação
- **Indisponibilidade**: SLA com fornecedores + contingência

---

## 8. RECURSOS E INVESTIMENTO

### 8.1 Time Necessário
- **Product Owner**: 1 pessoa (7 meses)
- **Tech Lead**: 1 pessoa (7 meses)  
- **Desenvolvedores Senior**: 3 pessoas (7 meses)
- **QA Engineer**: 1 pessoa (5 meses)
- **DevOps Engineer**: 1 pessoa (3 meses)

### 8.2 Infraestrutura
- **Servidores**: 3 VMs (App, DB, Cache)
- **Storage**: 2TB inicial + crescimento
- **Network**: Links dedicados custodiantes
- **Licenças**: SQL Server, monitoring tools

### 8.3 Investimento Estimado
- **Desenvolvimento**: R$ 1.2M (time + 7 meses)
- **Infraestrutura**: R$ 200K (setup + 12 meses)
- **Licenças**: R$ 150K/ano
- **Total Ano 1**: R$ 1.55M

### 8.4 ROI Esperado
- **Economia operacional**: R$ 2M/ano
- **Redução de risco**: R$ 500K/ano
- **ROI**: 161% no primeiro ano
- **Payback**: 7.4 meses

---

## 9. PRÓXIMOS PASSOS

### 9.1 Aprovações Necessárias
- [ ] **Diretor de Tecnologia**: Arquitetura e investimento
- [ ] **Diretor de Risk**: Metodologia de conciliação  
- [ ] **Compliance**: Adequação regulatória
- [ ] **Jurídico**: Contratos com custodiantes

### 9.2 Ações Imediatas
1. **Definir sponsor executivo** do projeto
2. **Formar squad** multidisciplinar  
3. **Iniciar negociações** com custodiantes
4. **Validar arquitetura** com arquitetos BTG
5. **Elaborar cronograma** detalhado

### 9.3 Critérios de Go/No-Go
- ✅ **Budget aprovado**: R$ 1.55M ano 1
- ✅ **Time alocado**: 7 FTEs por 7 meses
- ✅ **Acordos custodiantes**: Mín. 3 principais
- ✅ **Sponsor executivo**: C-level commitment
- ✅ **Infraestrutura**: Ambientes disponíveis

---

**Documento preparado por**: Sistema POAgent  
**Baseado em**: Regulamentação AMBIMA, CVM e melhores práticas do mercado  
**Versão**: 1.0  
**Data**: 25/07/2025