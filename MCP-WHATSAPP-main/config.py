import os
from dotenv import load_dotenv

load_dotenv()

# Configurações da API do WhatsApp
WHATSAPP_API_TOKEN = os.getenv("WHATSAPP_API_TOKEN")
WHATSAPP_WEBHOOK_URL = os.getenv("WHATSAPP_WEBHOOK_URL", "http://localhost:8000/webhook")

# Configurações do OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Configurações do banco de dados
DB_FILE = os.getenv("DB_FILE", "clientes.json")

# Configurações do servidor
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 8000

# Configurações de CORS
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000"
]

# Configurações de CORS (alternativa)
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

# Configurações de Autenticação
JWT_SECRET = os.getenv("JWT_SECRET", "sua_chave_secreta_aqui")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Configurações do WhatsApp
WHATSAPP_API_URL = "https://graph.facebook.com/v17.0"
WHATSAPP_API_KEY = os.getenv("WHATSAPP_API_KEY")

# Configurações do Rate Limiter
MAX_REQUESTS_PER_MINUTE = 60
RATE_LIMIT_WINDOW = 60  # segundos
RATE_LIMIT_MESSAGE = "Você fez muitas requisições. Por favor, aguarde um momento."

# Configurações do Banco de Dados
DATABASE_URL = "sqlite:///./serralheria.db"

# Configurações de Logging
LOG_LEVEL = "INFO"
LOG_FILE = "serralheria_bot.log"

# Configurações de Mensagens
DEFAULT_WELCOME_MESSAGE = "Olá! Como posso ajudar você hoje?"
DEFAULT_ERROR_MESSAGE = "Desculpe, ocorreu um erro. Por favor, tente novamente mais tarde."

# Configurações dos agentes
AGENT_CONFIG = {
    "atendente": {
        "model": "gpt-3.5-turbo",
        "temperature": 0.7,
        "max_tokens": 500
    },
    "vendedor": {
        "model": "gpt-3.5-turbo",
        "temperature": 0.7,
        "max_tokens": 500
    }
}

# Mensagens padrão
MENSAGENS = {
    "boas_vindas": "Olá! Sou o assistente virtual da Serralheria. Como posso ajudar você hoje?",
    "orcamento_solicitado": "Vou preparar um orçamento para você. Por favor, me informe as medidas do portão desejado.",
    "visita_agendada": "Visita técnica agendada com sucesso! Um de nossos vendedores entrará em contato para confirmar.",
    "erro": "Desculpe, ocorreu um erro. Por favor, tente novamente mais tarde."
}

# Diretórios
DIRETORIOS = {
    "imagens": "portoes",
    "logs": "logs",
    "temp": "temp"
}

# Criar diretórios se não existirem
for diretorio in DIRETORIOS.values():
    os.makedirs(diretorio, exist_ok=True) 