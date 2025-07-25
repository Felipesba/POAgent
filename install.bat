@echo off
REM Script de instalação do POAgent para Windows
REM Sistema de Geração de PRDs e Features para Carteira de Custódia Brasileira

echo 🚀 Iniciando instalação do POAgent...

REM Verificar Python
echo 📋 Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não encontrado. Por favor, instale Python 3.8+ primeiro.
    pause
    exit /b 1
)

python -c "import sys; print('✅ Python ' + '.'.join(map(str, sys.version_info[:2])) + ' encontrado')"

REM Verificar versão do Python
python -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"
if errorlevel 1 (
    echo ❌ Python 3.8+ é necessário
    pause
    exit /b 1
)

REM Criar ambiente virtual
echo 🔧 Criando ambiente virtual...
if not exist "venv" (
    python -m venv venv
    echo ✅ Ambiente virtual criado
) else (
    echo ✅ Ambiente virtual já existe
)

REM Ativar ambiente virtual
echo 🔌 Ativando ambiente virtual...
call venv\Scripts\activate.bat

REM Atualizar pip
echo 📦 Atualizando pip...
python -m pip install --upgrade pip

REM Instalar dependências
echo 📚 Instalando dependências...
if exist "requirements.txt" (
    pip install -r requirements.txt
    echo ✅ Dependências instaladas
) else (
    echo ❌ Arquivo requirements.txt não encontrado
    pause
    exit /b 1
)

REM Criar diretórios necessários
echo 📁 Criando estrutura de diretórios...
if not exist "data\chroma_db" mkdir data\chroma_db
if not exist "documents" mkdir documents
if not exist "output" mkdir output
if not exist "logs" mkdir logs
echo ✅ Diretórios criados

REM Configurar arquivo .env
echo ⚙️ Configurando ambiente...
if not exist ".env" (
    if exist ".env.example" (
        copy .env.example .env >nul
        echo ✅ Arquivo .env criado a partir do .env.example
        echo ⚠️  IMPORTANTE: Configure sua OPENAI_API_KEY no arquivo .env
    ) else (
        echo ❌ Arquivo .env.example não encontrado
        pause
        exit /b 1
    )
) else (
    echo ✅ Arquivo .env já existe
)

REM Verificar se a chave da OpenAI está configurada
findstr "your_openai_api_key_here" .env >nul
if not errorlevel 1 (
    echo ⚠️  ATENÇÃO: Configure sua chave da OpenAI no arquivo .env antes de usar o sistema
)

REM Inicializar base de dados
echo 🗄️ Inicializando base de dados...
python main.py setup-database 2>nul || (
    echo ⚠️  Aviso: Não foi possível inicializar a base de dados automaticamente
    echo    Execute 'python main.py setup-database' após configurar a API key
)

echo.
echo 🎉 Instalação concluída com sucesso!
echo.
echo 📋 Próximos passos:
echo 1. Configure sua OPENAI_API_KEY no arquivo .env
echo 2. Ative o ambiente virtual: venv\Scripts\activate.bat
echo 3. Execute: python main.py --help para ver os comandos disponíveis
echo.
echo 📖 Exemplos de uso:
echo    python main.py upload-document --file-path documento.pdf --file-type pdf
echo    python main.py generate-prd --request "Sistema de custódia CVM"
echo    python main.py generate-features --request "API de consulta de saldos"
echo.
echo 📚 Consulte o README.md para documentação completa
echo.
pause