from fastapi import FastAPI, Request
from serralheria_agent import SerralheriaAgent
import uvicorn
from typing import Dict
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
agente = SerralheriaAgent()

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    
    # Processar mensagem recebida
    if 'messages' in data:
        for message in data['messages']:
            if message['type'] == 'text':
                numero_cliente = message['from']
                mensagem = message['body']
                
                # Processar mensagem com o agente
                resposta = agente.processar_mensagem(mensagem)
                
                # Aqui você implementaria a lógica para enviar a resposta via WhatsApp
                # usando a API do WhatsApp Business
                
                return {"status": "success", "message": "Mensagem processada"}
    
    return {"status": "error", "message": "Formato de mensagem inválido"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 