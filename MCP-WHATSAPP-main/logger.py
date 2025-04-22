import logging
import os
from datetime import datetime
from config import LOG_LEVEL, LOG_FILE

# Configurar o logger
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

# Criar loggers
agent_logger = logging.getLogger('serralheria_agent')
whatsapp_logger = logging.getLogger('whatsapp_api')

def log_message(logger: logging.Logger, level: str, message: str, **kwargs):
    """
    Função auxiliar para logar mensagens com diferentes níveis
    """
    log_levels = {
        'debug': logger.debug,
        'info': logger.info,
        'warning': logger.warning,
        'error': logger.error,
        'critical': logger.critical
    }
    
    log_func = log_levels.get(level.lower(), logger.info)
    log_func(message, **kwargs) 