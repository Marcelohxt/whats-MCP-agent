from openai import OpenAI
from config import OPENAI_API_KEY, AGENT_CONFIG

class SerralheriaAgent:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.config = AGENT_CONFIG

    def processar_mensagem(self, mensagem: str, tipo_agente: str = "atendente") -> str:
        """Processa a mensagem usando o OpenAI API"""
        try:
            config = self.config[tipo_agente]
            response = self.client.chat.completions.create(
                model=config["model"],
                messages=[
                    {"role": "system", "content": "Você é um assistente virtual de uma serralheria, especializado em orçamentos e agendamentos."},
                    {"role": "user", "content": mensagem}
                ],
                temperature=config["temperature"],
                max_tokens=config["max_tokens"]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Erro ao processar mensagem: {str(e)}")
            return "Desculpe, ocorreu um erro ao processar sua mensagem."

    def gerar_orcamento(self, detalhes: str) -> str:
        """Gera um orçamento baseado nos detalhes fornecidos"""
        try:
            response = self.client.chat.completions.create(
                model=self.config["vendedor"]["model"],
                messages=[
                    {"role": "system", "content": "Você é um especialista em orçamentos de serralheria."},
                    {"role": "user", "content": f"Gere um orçamento para: {detalhes}"}
                ],
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Erro ao gerar orçamento: {str(e)}")
            return "Desculpe, ocorreu um erro ao gerar o orçamento."

    def agendar_visita(self, detalhes: str) -> str:
        """Processa um agendamento de visita"""
        try:
            response = self.client.chat.completions.create(
                model=self.config["atendente"]["model"],
                messages=[
                    {"role": "system", "content": "Você é um assistente especializado em agendamentos."},
                    {"role": "user", "content": f"Processe este agendamento: {detalhes}"}
                ],
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Erro ao agendar visita: {str(e)}")
            return "Desculpe, ocorreu um erro ao agendar a visita."

if __name__ == "__main__":
    # Exemplo de uso
    agente = SerralheriaAgent()
    resposta = agente.processar_mensagem("Olá, preciso de um orçamento para um portão de ferro")
    print(resposta) 