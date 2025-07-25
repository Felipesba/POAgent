# Contribuindo para POAgent

Obrigado por considerar contribuir para o POAgent! 🎉

## 🚀 Como Contribuir

### 1. Fork e Clone
```bash
# Fork o repositório no GitHub
# Clone seu fork
git clone https://github.com/seu-usuario/POAgent.git
cd POAgent
```

### 2. Configure o Ambiente
```bash
# Instale as dependências
./install.sh

# Configure as variáveis de ambiente
cp .env.example .env
# Edite .env com suas configurações
```

### 3. Crie uma Branch
```bash
git checkout -b feature/nova-funcionalidade
# ou
git checkout -b fix/correcao-bug
```

### 4. Faça suas Alterações
- Siga os padrões de código existentes
- Adicione testes para novas funcionalidades
- Atualize a documentação se necessário

### 5. Teste suas Alterações
```bash
# Execute os testes
python -m pytest tests/

# Teste manualmente
python main.py --help
```

### 6. Commit e Push
```bash
git add .
git commit -m "feat: adiciona nova funcionalidade X"
git push origin feature/nova-funcionalidade
```

### 7. Abra um Pull Request
- Descreva claramente as mudanças
- Referencie issues relacionadas
- Inclua screenshots se aplicável

## 📝 Padrões de Commit

Usamos [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` nova funcionalidade
- `fix:` correção de bug
- `docs:` apenas documentação
- `style:` formatação, sem mudança de código
- `refactor:` refatoração de código
- `test:` adição ou correção de testes
- `chore:` mudanças em ferramentas, configurações

## 🐛 Reportando Bugs

1. Verifique se o bug já foi reportado
2. Use o template de issue
3. Inclua informações do sistema
4. Forneça passos para reproduzir

## 💡 Sugerindo Funcionalidades

1. Verifique se não existe uma solicitação similar
2. Descreva o problema que resolve
3. Proponha uma solução
4. Considere implementações alternativas

## 🔧 Desenvolvimento

### Estrutura do Projeto
```
POAgent/
├── src/
│   ├── agents/          # Agentes especializados
│   ├── tasks/           # Tasks dos agentes
│   ├── tools/           # Tools personalizadas
│   └── utils/           # Utilitários
├── tests/               # Testes automatizados
├── docs/                # Documentação
└── output/              # Arquivos gerados
```

### Adicionando Novos Agentes
1. Crie em `src/agents/`
2. Implemente interface base
3. Adicione testes
4. Atualize documentação

### Adicionando Novas Tools
1. Crie em `src/tools/`
2. Herde de `BaseTool`
3. Implemente `_run()` method
4. Adicione validação de entrada

## 🧪 Testes

```bash
# Testes unitários
python -m pytest tests/unit/

# Testes de integração
python -m pytest tests/integration/

# Coverage
python -m pytest --cov=src tests/
```

## 📖 Documentação

- Docstrings em português
- Comentários explicativos em código complexo
- Exemplos de uso na documentação
- README atualizado para novas funcionalidades

## ❓ Dúvidas?

- Abra uma [Discussion](https://github.com/seu-usuario/POAgent/discussions)
- Entre no Discord (link no README)
- Envie email: contato@seu-dominio.com

Obrigado por contribuir! 🙏