import requests
from typing import Dict, List, Optional
from config import WHATSAPP_API_KEY, WHATSAPP_API_URL
from logger import agent_logger, log_message

class WhatsAppSender:
    def __init__(self):
        self.api_key = WHATSAPP_API_KEY
        self.base_url = WHATSAPP_API_URL
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def enviar_mensagem_texto(self, numero: str, mensagem: str) -> bool:
        """Envia uma mensagem de texto para um número de WhatsApp"""
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
                log_message(agent_logger, "info", f"Mensagem enviada para {numero}")
                return True
            else:
                log_message(agent_logger, "error", 
                          f"Erro ao enviar mensagem: {response.status_code} - {response.text}")
                return False

        except Exception as e:
            log_message(agent_logger, "error", f"Exceção ao enviar mensagem: {str(e)}")
            return False

    def enviar_imagem(self, numero: str, url_imagem: str, legenda: Optional[str] = None) -> bool:
        """Envia uma imagem para um número de WhatsApp"""
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
                log_message(agent_logger, "info", f"Imagem enviada para {numero}")
                return True
            else:
                log_message(agent_logger, "error", 
                          f"Erro ao enviar imagem: {response.status_code} - {response.text}")
                return False

        except Exception as e:
            log_message(agent_logger, "error", f"Exceção ao enviar imagem: {str(e)}")
            return False

    def enviar_orcamento(self, numero: str, detalhes: Dict) -> bool:
        """Envia um orçamento formatado para o cliente"""
        try:
            mensagem = f"""*Orçamento para Portão*
            
Tipo: {detalhes['tipo_portao']}
Medidas: {detalhes['medidas']['largura']}m x {detalhes['medidas']['altura']}m
Valor: R$ {detalhes['valor']:.2f}

Para agendar uma visita técnica, responda com 'AGENDAR'."""
            
            return self.enviar_mensagem_texto(numero, mensagem)

        except Exception as e:
            log_message(agent_logger, "error", f"Exceção ao enviar orçamento: {str(e)}")
            return False

    def confirmar_visita(self, numero: str, data: str, horario: str) -> bool:
        """Envia confirmação de visita técnica"""
        try:
            mensagem = f"""*Visita Técnica Agendada*
            
Data: {data}
Horário: {horario}

Um de nossos vendedores entrará em contato para confirmar a visita."""
            
            return self.enviar_mensagem_texto(numero, mensagem)

        except Exception as e:
            log_message(agent_logger, "error", f"Exceção ao confirmar visita: {str(e)}")
            return False 