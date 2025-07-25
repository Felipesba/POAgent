#!/bin/bash

# Script de instalação do POAgent
# Sistema de Geração de PRDs e Features para Carteira de Custódia Brasileira

set -e  # Parar em caso de erro

echo "🚀 Iniciando instalação do POAgent..."

# Verificar Python
echo "📋 Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Por favor, instale Python 3.8+ primeiro."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✅ Python $PYTHON_VERSION encontrado"

# Verificar se a versão é compatível
python3 -c "
import sys
if sys.version_info < (3, 8):
    print('❌ Python 3.8+ é necessário. Versão atual:', sys.version_info[:2])
    sys.exit(1)
"

# Criar ambiente virtual
echo "🔧 Criando ambiente virtual..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Ambiente virtual criado"
else
    echo "✅ Ambiente virtual já existe"
fi

# Ativar ambiente virtual
echo "🔌 Ativando ambiente virtual..."
source venv/bin/activate

# Atualizar pip
echo "📦 Atualizando pip..."
pip install --upgrade pip

# Instalar dependências
echo "📚 Instalando dependências..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "✅ Dependências instaladas"
else
    echo "❌ Arquivo requirements.txt não encontrado"
    exit 1
fi

# Criar diretórios necessários
echo "📁 Criando estrutura de diretórios..."
mkdir -p data/chroma_db
mkdir -p documents
mkdir -p output
mkdir -p logs
echo "✅ Diretórios criados"

# Configurar arquivo .env
echo "⚙️ Configurando ambiente..."
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "✅ Arquivo .env criado a partir do .env.example"
        echo "⚠️  IMPORTANTE: Configure sua OPENAI_API_KEY no arquivo .env"
    else
        echo "❌ Arquivo .env.example não encontrado"
        exit 1
    fi
else
    echo "✅ Arquivo .env já existe"
fi

# Verificar se a chave da OpenAI está configurada
if grep -q "your_openai_api_key_here" .env; then
    echo "⚠️  ATENÇÃO: Configure sua chave da OpenAI no arquivo .env antes de usar o sistema"
fi

# Inicializar base de dados
echo "🗄️ Inicializando base de dados..."
python main.py setup-database || {
    echo "⚠️  Aviso: Não foi possível inicializar a base de dados automaticamente"
    echo "   Execute 'python main.py setup-database' após configurar a API key"
}

# Tornar main.py executável
chmod +x main.py

echo ""
echo "🎉 Instalação concluída com sucesso!"
echo ""
echo "📋 Próximos passos:"
echo "1. Configure sua OPENAI_API_KEY no arquivo .env"
echo "2. Ative o ambiente virtual: source venv/bin/activate"
echo "3. Execute: python main.py --help para ver os comandos disponíveis"
echo ""
echo "📖 Exemplos de uso:"
echo "   python main.py upload-document --file-path documento.pdf --file-type pdf"
echo "   python main.py generate-prd --request 'Sistema de custódia CVM'"
echo "   python main.py generate-features --request 'API de consulta de saldos'"
echo ""
echo "📚 Consulte o README.md para documentação completa"