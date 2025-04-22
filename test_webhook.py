import requests
import json

url = "http://127.0.0.1:3000/webhook"
headers = {"Content-Type": "application/json"}
data = {
    "messages": [
        {
            "from": "5511930779357",
            "type": "text",
            "body": "Olá, preciso de um orçamento para um portão"
        }
    ]
}

response = requests.post(url, headers=headers, json=data)
print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}") 