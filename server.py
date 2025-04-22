from fastapi import FastAPI, Request
import uvicorn
import json
from datetime import datetime
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Configurações do WhatsApp
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
WHATSAPP_URL = "https://graph.facebook.com/v17.0/YOUR_PHONE_NUMBER_ID/messages"  # Você precisará substituir YOUR_PHONE_NUMBER_ID

def send_whatsapp_message(to: str, message: str):
    """Envia mensagem para o WhatsApp"""
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    
    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": message}
    }
    
    response = requests.post(WHATSAPP_URL, headers=headers, json=data)
    return response.json()

def process_command(message: str) -> str:
    """Processa comandos e retorna uma resposta apropriada"""
    message = message.lower()
    
    if message == "hora":
        return f"Agora são: {datetime.now().strftime('%H:%M:%S')}"
    elif message == "data":
        return f"Hoje é: {datetime.now().strftime('%d/%m/%Y')}"
    elif message == "ajuda":
        return "Comandos disponíveis:\n- hora: mostra a hora atual\n- data: mostra a data atual\n- ajuda: mostra esta mensagem"
    else:
        return f"Recebi sua mensagem: {message}\nUse 'ajuda' para ver os comandos disponíveis"

@app.post("/webhook")
async def webhook(request: Request):
    """Endpoint para receber mensagens do WhatsApp"""
    try:
        # Verificação do webhook
        data = await request.json()
        
        # Se for uma mensagem de verificação do webhook
        if data.get("object"):
            if data.get("entry") and data["entry"][0].get("changes") and \
               data["entry"][0]["changes"][0].get("value") and \
               data["entry"][0]["changes"][0]["value"].get("messages"):
                
                phone_number_id = data["entry"][0]["changes"][0]["value"]["metadata"]["phone_number_id"]
                from_number = data["entry"][0]["changes"][0]["value"]["messages"][0]["from"]
                msg_body = data["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]

                print(f"\nMensagem recebida de {from_number}: {msg_body}")
                
                # Processa o comando e envia resposta
                resposta = process_command(msg_body)
                send_whatsapp_message(from_number, resposta)
                
                return {"status": "success", "message": "Mensagem processada"}

        return {"status": "error", "message": "Formato de mensagem não reconhecido"}

    except Exception as e:
        print(f"\nErro ao processar requisição: {str(e)}")
        return {"status": "error", "message": str(e)}

@app.get("/webhook")
async def verify_webhook(request: Request):
    """Endpoint para verificação do webhook pelo WhatsApp"""
    try:
        # Obtém os parâmetros da query
        params = dict(request.query_params)
        
        # Verifica o token
        verify_token = os.getenv("VERIFY_TOKEN")
        mode = params.get("hub.mode")
        token = params.get("hub.verify_token")
        challenge = params.get("hub.challenge")

        if mode and token:
            if mode == "subscribe" and token == verify_token:
                print("Webhook verificado!")
                return int(challenge)
            else:
                return {"status": "error", "message": "Verificação falhou"}

        return {"status": "error", "message": "Parâmetros inválidos"}

    except Exception as e:
        print(f"\nErro na verificação do webhook: {str(e)}")
        return {"status": "error", "message": str(e)}

@app.get("/")
async def root():
    """Rota de teste para verificar se o servidor está online"""
    return {
        "status": "online", 
        "message": "Servidor webhook está funcionando",
        "comandos_disponíveis": [
            "hora - mostra a hora atual",
            "data - mostra a data atual",
            "ajuda - lista todos os comandos"
        ]
    }

if __name__ == "__main__":
    print("=== Iniciando servidor webhook ===")
    print("Servidor estará disponível em: http://localhost:3000")
    print("Comandos disponíveis: hora, data, ajuda")
    uvicorn.run(app, host="localhost", port=3000) 