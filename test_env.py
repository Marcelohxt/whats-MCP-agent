from dotenv import load_dotenv
import os

load_dotenv()

# Tenta ler a chave da API
api_key = os.getenv("OPENAI_API_KEY")

print("OpenAI API Key:", "***" + api_key[-4:] if api_key else "Não encontrada") 