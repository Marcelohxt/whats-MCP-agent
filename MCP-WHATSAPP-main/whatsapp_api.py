import requests
from typing import Dict, Optional
from config import WHATSAPP_API_TOKEN, WHATSAPP_WEBHOOK_URL
from logger import whatsapp_logger, log_message

class WhatsAppAPI:
    def __init__(self):
        self.api_token = WHATSAPP_API_TOKEN
        self.base_url = "https://graph.facebook.com/v17.0"
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }

    def enviar_mensagem(self, numero: str, mensagem: str) -> bool:
        """Envia uma mensagem de texto"""
        try:
            payload = {
                "messaging_product": "whatsapp",
                "to": numero,
                "type": "text",
                "text": {"body": mensagem}
            }

            response = requests.post(
                f"{self.base_url}/messages",
                headers=self.headers,
                json=payload
            )

            if response.status_code == 200:
                log_message(whatsapp_logger, "info", f"Mensagem enviada para {numero}")
                return True
            else:
                log_message(whatsapp_logger, "error", 
                          f"Erro ao enviar mensagem: {response.status_code} - {response.text}")
                return False

        except Exception as e:
            log_message(whatsapp_logger, "error", f"Exceção ao enviar mensagem: {str(e)}")
            return False

    def enviar_imagem(self, numero: str, url_imagem: str, legenda: Optional[str] = None) -> bool:
        """Envia uma imagem"""
        try:
            payload = {
                "messaging_product": "whatsapp",
                "to": numero,
                "type": "image",
                "image": {
                    "link": url_imagem
                }
            }

            if legenda:
                payload["image"]["caption"] = legenda

            response = requests.post(
                f"{self.base_url}/messages",
                headers=self.headers,
                json=payload
            )

            if response.status_code == 200:
                log_message(whatsapp_logger, "info", f"Imagem enviada para {numero}")
                return True
            else:
                log_message(whatsapp_logger, "error", 
                          f"Erro ao enviar imagem: {response.status_code} - {response.text}")
                return False

        except Exception as e:
            log_message(whatsapp_logger, "error", f"Exceção ao enviar imagem: {str(e)}")
            return False

    def enviar_template(self, numero: str, nome_template: str, parametros: Dict) -> bool:
        """Envia uma mensagem usando um template"""
        try:
            payload = {
                "messaging_product": "whatsapp",
                "to": numero,
                "type": "template",
                "template": {
                    "name": nome_template,
                    "language": {
                        "code": "pt_BR"
                    },
                    "components": []
                }
            }

            # Adicionar parâmetros ao template
            for chave, valor in parametros.items():
                payload["template"]["components"].append({
                    "type": "body",
                    "parameters": [
                        {
                            "type": "text",
                            "text": str(valor)
                        }
                    ]
                })

            response = requests.post(
                f"{self.base_url}/messages",
                headers=self.headers,
                json=payload
            )

            if response.status_code == 200:
                log_message(whatsapp_logger, "info", f"Template enviado para {numero}")
                return True
            else:
                log_message(whatsapp_logger, "error", 
                          f"Erro ao enviar template: {response.status_code} - {response.text}")
                return False

        except Exception as e:
            log_message(whatsapp_logger, "error", f"Exceção ao enviar template: {str(e)}")
            return False

    def verificar_status_mensagem(self, message_id: str) -> Optional[Dict]:
        """Verifica o status de uma mensagem enviada"""
        try:
            response = requests.get(
                f"{self.base_url}/{message_id}",
                headers=self.headers
            )

            if response.status_code == 200:
                return response.json()
            else:
                log_message(whatsapp_logger, "error", 
                          f"Erro ao verificar status: {response.status_code} - {response.text}")
                return None

        except Exception as e:
            log_message(whatsapp_logger, "error", f"Exceção ao verificar status: {str(e)}")
            return None

    def configurar_webhook(self, url: str) -> bool:
        """Configura o webhook para receber notificações"""
        try:
            payload = {
                "url": url,
                "fields": ["messages"]
            }

            response = requests.post(
                f"{self.base_url}/webhooks",
                headers=self.headers,
                json=payload
            )

            if response.status_code == 200:
                log_message(whatsapp_logger, "info", "Webhook configurado com sucesso")
                return True
            else:
                log_message(whatsapp_logger, "error", 
                          f"Erro ao configurar webhook: {response.status_code} - {response.text}")
                return False

        except Exception as e:
            log_message(whatsapp_logger, "error", f"Exceção ao configurar webhook: {str(e)}")
            return False 