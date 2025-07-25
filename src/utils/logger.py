"""
Sistema de logging configurável
"""

import logging
import os
from datetime import datetime

def setup_logger(name: str, level: str = None) -> logging.Logger:
    """Configurar logger com formatação padronizada"""
    
    # Determinar nível de log
    log_level = level or os.getenv('LOG_LEVEL', 'INFO')
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    
    # Criar logger
    logger = logging.getLogger(name)
    logger.setLevel(numeric_level)
    
    # Evitar duplicação de handlers
    if logger.handlers:
        return logger
    
    # Criar formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler para console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Handler para arquivo (opcional)
    if os.getenv('LOG_TO_FILE', 'false').lower() == 'true':
        log_dir = os.getenv('LOG_DIRECTORY', 'logs')
        os.makedirs(log_dir, exist_ok=True)
        
        log_file = os.path.join(log_dir, f"custody_prd_{datetime.now().strftime('%Y%m%d')}.log")
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(numeric_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger