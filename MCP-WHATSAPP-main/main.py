from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from config import (
    SERVER_HOST, SERVER_PORT, CORS_ORIGINS,
    MAX_REQUESTS_PER_MINUTE, RATE_LIMIT_WINDOW,
    RATE_LIMIT_MESSAGE, WHATSAPP_API_KEY
)
from rate_limiter import RateLimiter
from serralheria_agent import SerralheriaAgent
from whatsapp_sender import WhatsAppSender
import uvicorn

app = FastAPI()

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializa os componentes
rate_limiter = RateLimiter()
serralheria_agent = SerralheriaAgent()
whatsapp_sender = WhatsAppSender()

async def check_rate_limit(request: Request):
    client_id = request.client.host
    allowed, time_remaining = rate_limiter.is_allowed(client_id)
    
    if not allowed:
        raise HTTPException(
            status_code=429,
            detail={
                "message": RATE_LIMIT_MESSAGE,
                "retry_after": time_remaining
            }
        )
    
    return True

@app.get("/")
async def root():
    return {"message": "API da Serralheria"}

@app.get("/api/status")
async def status(rate_limit: bool = Depends(check_rate_limit)):
    return {"status": "online"}

@app.post("/webhook")
async def whatsapp_webhook(request: Request, rate_limit: bool = Depends(check_rate_limit)):
    try:
        data = await request.json()
        
        # Verificar se é uma mensagem válida do WhatsApp
        if 'messages' not in data:
            return JSONResponse(content={"status": "error", "message": "Formato inválido"})
        
        for message in data['messages']:
            if message['type'] == 'text':
                numero = message['from']
                mensagem = message['body']
                
                # Processar a mensagem com o agente
                resposta = serralheria_agent.processar_mensagem(mensagem)
                
                # Enviar resposta via WhatsApp
                whatsapp_sender.enviar_mensagem_texto(numero, resposta)
        
        return JSONResponse(content={"status": "success"})
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )

if __name__ == "__main__":
    uvicorn.run(app, host=SERVER_HOST, port=SERVER_PORT) 