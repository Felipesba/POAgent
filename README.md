# Sistema de Geração de PRDs e Features para Carteira de Custódia Brasileira

Sistema inteligente baseado em CrewAI para geração de PRDs (Product Requirements Documents) e especificações técnicas de features para soluções de custódia de ativos no Brasil, com processamento avançado de documentos regulatórios.

## 🚀 Funcionalidades

### Processamento Inteligente de Documentos
- **Suporte a múltiplos formatos**: PDFs, TXT e URLs
- **Processamento de PDFs**: PyMuPDF com fallback para pypdf
- **Indexação semântica**: ChromaDB com embeddings SentenceTransformers
- **Busca inteligente**: Consultas semânticas nos documentos indexados

### Agentes Especializados
1. **Document Intelligence Agent**: Processa legislação CVM/BACEN/AMBIMA
2. **Product Strategy Agent**: Cria PRDs customizados baseados nos documentos
3. **Feature Engineering Agent**: Gera especificações técnicas detalhadas

### Interface CLI Completa
- Upload e processamento de documentos
- Geração de PRDs
- Geração de features
- Análise de compliance
- Listagem de documentos indexados

## 📋 Pré-requisitos

- Python 3.8+
- OpenAI API Key
- 4GB+ RAM disponível para processamento de embeddings

## 🛠️ Instalação

### 1. Clone o repositório
```bash
git clone <repository-url>
cd POAgent
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Configure as variáveis de ambiente
```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas configurações:
```env
OPENAI_API_KEY=sua_chave_openai_aqui
OPENAI_MODEL_NAME=gpt-4-turbo-preview
CHROMA_PERSIST_DIRECTORY=./data/chroma_db
DOCUMENTS_DIRECTORY=./documents
EMBEDDINGS_MODEL=all-MiniLM-L6-v2
```

### 4. Inicialize a base de dados
```bash
python main.py setup-database
```

## 📖 Guia de Uso

### Upload de Documentos

#### PDFs de Regulamentação
```bash
python main.py upload-document --file-path ./docs/resolucao_cvm_35.pdf --file-type pdf
```

#### Arquivos de Texto
```bash
python main.py upload-document --file-path ./docs/norma_bacen.txt --file-type txt
```

#### Links Externos
```bash
python main.py upload-document --file-path "https://www.cvm.gov.br/legislacao/resolucoes/anexos/res035.pdf" --file-type url
```

### Geração de PRDs

```bash
python main.py generate-prd --request "Criar sistema de custódia para fundos de investimento conforme CVM 35/2021"
```

Com contexto adicional:
```bash
python main.py generate-prd --request "Sistema de liquidação automática" --context "Integração com SELIC e B3"
```

### Geração de Features

```bash
python main.py generate-features --request "API de consulta de saldos em tempo real"
```

### Análise de Compliance

```bash
python main.py analyze-compliance --regulation-area "segregação patrimonial"
```

### Listar Documentos Indexados

```bash
python main.py list-documents
```

## 🏗️ Arquitetura do Sistema

```
POAgent/
├── src/
│   ├── agents/                 # Agentes especializados
│   │   ├── document_intelligence_agent.py
│   │   ├── product_strategy_agent.py
│   │   └── feature_engineering_agent.py
│   ├── tasks/                  # Tasks para cada tipo de análise
│   │   ├── document_analysis_tasks.py
│   │   ├── prd_generation_tasks.py
│   │   └── feature_engineering_tasks.py
│   ├── tools/                  # Tools personalizadas
│   │   ├── document_search_tool.py
│   │   ├── context_generator_tool.py
│   │   └── regulation_analyzer_tool.py
│   ├── utils/                  # Utilitários
│   │   ├── logger.py
│   │   └── text_splitter.py
│   ├── document_processor.py   # Processador principal
│   └── crew.py                # Sistema CrewAI
├── main.py                    # Interface CLI
├── requirements.txt
└── README.md
```

## 🤖 Agentes Disponíveis

### Document Intelligence Agent
- **Especialidade**: Análise de documentos regulatórios
- **Conhecimento**: CVM, BACEN, AMBIMA
- **Funções**: Extração de requisitos, identificação de obrigações

### Product Strategy Agent  
- **Especialidade**: Estratégia de produto e PRDs
- **Conhecimento**: Mercado financeiro brasileiro
- **Funções**: Business analysis, market research, PRD generation

### Feature Engineering Agent
- **Especialidade**: Especificações técnicas
- **Conhecimento**: Arquitetura de sistemas financeiros
- **Funções**: Feature specs, API design, database design

## 🔧 Configurações Avançadas

### Customização de Embeddings
```env
EMBEDDINGS_MODEL=all-MiniLM-L6-v2  # Modelo padrão
# Alternativas:
# EMBEDDINGS_MODEL=paraphrase-multilingual-MiniLM-L12-v2  # Melhor para português
# EMBEDDINGS_MODEL=all-mpnet-base-v2  # Maior qualidade, mais lento
```

### Ajuste de Chunking
No arquivo `src/utils/text_splitter.py`:
```python
chunk_size = 1000      # Tamanho do chunk em tokens
chunk_overlap = 200    # Overlap entre chunks
```

### Logging
```env
LOG_LEVEL=INFO
LOG_TO_FILE=true
LOG_DIRECTORY=./logs
```

## 📊 Exemplos de Uso

### Caso 1: Análise de Nova Regulamentação
```bash
# 1. Upload da regulamentação
python main.py upload-document --file-path ./nova_resolucao_cvm.pdf --file-type pdf

# 2. Análise de compliance
python main.py analyze-compliance --regulation-area "nova resolução CVM custódia"

# 3. Geração de PRD para adequação
python main.py generate-prd --request "Adequar sistema à nova resolução CVM sobre custódia qualificada"
```

### Caso 2: Nova Feature de API
```bash
# 1. Geração de especificação
python main.py generate-features --request "API GraphQL para consulta de posições consolidadas"

# 2. Com contexto específico
python main.py generate-features --request "Endpoint de reconciliação diária" --context "Integração com sistemas legados COBOL"
```

## 🔍 Troubleshooting

### Erro de API Key
```
❌ Erro: OpenAI API key não configurada
```
**Solução**: Configure `OPENAI_API_KEY` no arquivo `.env`

### Erro de Processamento de PDF
```
❌ Erro ao processar PDF: Cannot open file
```
**Solução**: Verifique se o arquivo existe e se tem permissões de leitura

### Erro de Base de Dados
```
❌ Erro: Collection not found
```
**Solução**: Execute `python main.py setup-database`

### Performance Lenta
- Reduza `chunk_size` para documentos grandes
- Use modelo de embedding menor
- Aumente RAM disponível

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 📞 Suporte

Para suporte técnico:
- Crie uma issue no GitHub
- Consulte a documentação dos logs em `./logs/`
- Verifique as configurações no `.env`

## 🔄 Roadmap

- [ ] Interface web com Streamlit
- [ ] Integração com APIs regulatórias
- [ ] Processamento de vídeos e áudios
- [ ] Análise de sentiment regulatório
- [ ] Dashboard de compliance
- [ ] Notificações automáticas de mudanças regulatórias