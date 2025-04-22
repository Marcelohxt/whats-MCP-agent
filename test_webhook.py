import requests
import json

# URL do webhook (usando a porta 8000 que está configurada)
url = "http://localhost:8000/webhook"

# Headers da requisição
headers = {
    "Content-Type": "application/json"
}

# Dados simulando uma mensagem do WhatsApp
data = {
    "messages": [
        {
            "from": "5511930779357",
            "type": "text",
            "body": "Olá, preciso de um orçamento para um portão basculante de 3x2.5 metros"
        }
    ]
}

try:
    # Enviando a requisição POST
    print("Enviando mensagem de teste...")
    response = requests.post(url, headers=headers, json=data)
    
    # Exibindo resultados
    print(f"\nStatus Code: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    print("\nResposta completa:")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)

except requests.exceptions.ConnectionError:
    print("\nErro: Não foi possível conectar ao servidor.")
    print("Verifique se o servidor está rodando em http://localhost:8000") 