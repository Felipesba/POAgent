#!/usr/bin/env python3
"""
Sistema de Geração de PRDs e Features para Carteira de Custódia Brasileira
usando CrewAI com processamento inteligente de documentos.
"""

import click
import os
from dotenv import load_dotenv
try:
    from src.crew import CustodyPRDCrew
    CREWAI_AVAILABLE = True
except ImportError:
    from src.simple_agents import SimpleCustodySystem
    CREWAI_AVAILABLE = False
from src.document_processor import DocumentProcessor
from src.utils.logger import setup_logger

load_dotenv()
logger = setup_logger(__name__)

@click.group()
def cli():
    """Sistema de Geração de PRDs e Features para Carteira de Custódia"""
    pass

@cli.command()
@click.option('--file-path', required=True, help='Caminho para o arquivo PDF, TXT ou URL')
@click.option('--file-type', type=click.Choice(['pdf', 'txt', 'url']), required=True, help='Tipo do documento')
def upload_document(file_path: str, file_type: str):
    """Upload e processamento de documentos"""
    try:
        processor = DocumentProcessor()
        result = processor.process_document(file_path, file_type)
        click.echo(f"✅ Documento processado com sucesso: {result['message']}")
        click.echo(f"📊 Chunks indexados: {result['chunks_count']}")
    except Exception as e:
        click.echo(f"❌ Erro ao processar documento: {str(e)}")
        logger.error(f"Erro no upload: {str(e)}")

@cli.command()
@click.option('--request', required=True, help='Descrição do pedido para PRD')
@click.option('--context', help='Contexto adicional (opcional)')
def generate_prd(request: str, context: str = None):
    """Gerar PRD baseado no pedido do usuário"""
    try:
        if CREWAI_AVAILABLE:
            crew = CustodyPRDCrew()
            result = crew.generate_prd(request, context)
        else:
            system = SimpleCustodySystem()
            result = system.generate_prd(request, context)
        
        # Salvar resultado
        output_file = f"output/prd_{hash(request) % 10000}.md"
        os.makedirs('output', exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result)
        
        click.echo(f"✅ PRD gerado com sucesso!")
        click.echo(f"📄 Salvo em: {output_file}")
        click.echo(f"\n{result[:500]}...")
        
    except Exception as e:
        click.echo(f"❌ Erro ao gerar PRD: {str(e)}")
        logger.error(f"Erro na geração de PRD: {str(e)}")

@cli.command()
@click.option('--request', required=True, help='Descrição da feature desejada')
@click.option('--context', help='Contexto adicional (opcional)')
def generate_features(request: str, context: str = None):
    """Gerar features detalhadas baseadas no pedido"""
    try:
        if CREWAI_AVAILABLE:
            crew = CustodyPRDCrew()
            result = crew.generate_features(request, context)
        else:
            system = SimpleCustodySystem()
            result = system.generate_features(request, context)
        
        # Salvar resultado
        output_file = f"output/features_{hash(request) % 10000}.md"
        os.makedirs('output', exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result)
        
        click.echo(f"✅ Features geradas com sucesso!")
        click.echo(f"📄 Salvo em: {output_file}")
        click.echo(f"\n{result[:500]}...")
        
    except Exception as e:
        click.echo(f"❌ Erro ao gerar features: {str(e)}")
        logger.error(f"Erro na geração de features: {str(e)}")

@cli.command()
@click.option('--regulation-area', required=True, help='Área regulatória para análise')
def analyze_compliance(regulation_area: str):
    """Análise focada em compliance regulatório"""
    try:
        if CREWAI_AVAILABLE:
            crew = CustodyPRDCrew()
            result = crew.analyze_compliance(regulation_area)
        else:
            system = SimpleCustodySystem()
            result = system.analyze_compliance(regulation_area)
        
        # Salvar resultado
        output_file = f"output/compliance_{hash(regulation_area) % 10000}.md"
        os.makedirs('output', exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result)
        
        click.echo(f"✅ Análise de compliance concluída!")
        click.echo(f"📄 Salvo em: {output_file}")
        click.echo(f"\n{result[:500]}...")
        
    except Exception as e:
        click.echo(f"❌ Erro na análise de compliance: {str(e)}")
        logger.error(f"Erro na análise de compliance: {str(e)}")

@cli.command()
def list_documents():
    """Listar documentos indexados"""
    try:
        processor = DocumentProcessor()
        docs = processor.list_indexed_documents()
        
        if not docs:
            click.echo("📭 Nenhum documento indexado encontrado.")
            return
            
        click.echo("📚 Documentos indexados:")
        for doc in docs:
            click.echo(f"  • {doc['filename']} ({doc['type']}) - {doc['chunks']} chunks")
            
    except Exception as e:
        click.echo(f"❌ Erro ao listar documentos: {str(e)}")

@cli.command()
def setup_database():
    """Inicializar base de dados vetorial"""
    try:
        processor = DocumentProcessor()
        processor.setup_vector_database()
        click.echo("✅ Base de dados inicializada com sucesso!")
    except Exception as e:
        click.echo(f"❌ Erro ao inicializar base de dados: {str(e)}")

if __name__ == '__main__':
    cli()