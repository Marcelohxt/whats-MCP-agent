from typing import Dict, Optional
from serralheria_agent import SerralheriaAgent
from clientes_db import ClientesDB
from portoes_data import calcular_orcamento
from whatsapp_sender import WhatsAppSender
from logger import agent_logger, log_message
from config import MENSAGENS
from message_utils import (
    extrair_medidas,
    identificar_tipo_portao,
    extrair_data_horario,
    formatar_mensagem_orcamento,
    formatar_mensagem_visita
)
from whatsapp_api import WhatsAppAPI

class MessageProcessor:
    def __init__(self):
        self.agent = SerralheriaAgent()
        self.db = ClientesDB()
        self.whatsapp = WhatsAppAPI()

    def processar_mensagem(self, numero: str, mensagem: str):
        """Processa uma mensagem recebida e envia a resposta"""
        try:
            # Registrar mensagem recebida
            log_message(agent_logger, "info", f"Mensagem recebida de {numero}: {mensagem}")

            # Processar mensagem com o agente
            resposta = self.agent.processar_mensagem(mensagem)

            # Enviar resposta
            self.whatsapp.enviar_mensagem(numero, resposta)

            # Registrar resposta enviada
            log_message(agent_logger, "info", f"Resposta enviada para {numero}: {resposta}")

        except Exception as e:
            log_message(agent_logger, "error", f"Erro ao processar mensagem: {str(e)}")
            # Enviar mensagem de erro genérica
            self.whatsapp.enviar_mensagem(numero, "Desculpe, ocorreu um erro ao processar sua mensagem.")

    def processar_orcamento(self, numero: str, detalhes: str):
        """Processa uma solicitação de orçamento"""
        try:
            orcamento = self.agent.gerar_orcamento(detalhes)
            self.whatsapp.enviar_mensagem(numero, orcamento)
            log_message(agent_logger, "info", f"Orçamento enviado para {numero}")
        except Exception as e:
            log_message(agent_logger, "error", f"Erro ao gerar orçamento: {str(e)}")
            self.whatsapp.enviar_mensagem(numero, "Desculpe, ocorreu um erro ao gerar o orçamento.")

    def processar_agendamento(self, numero: str, detalhes: str):
        """Processa uma solicitação de agendamento"""
        try:
            confirmacao = self.agent.agendar_visita(detalhes)
            self.whatsapp.enviar_mensagem(numero, confirmacao)
            log_message(agent_logger, "info", f"Agendamento processado para {numero}")
        except Exception as e:
            log_message(agent_logger, "error", f"Erro ao processar agendamento: {str(e)}")
            self.whatsapp.enviar_mensagem(numero, "Desculpe, ocorreu um erro ao processar o agendamento.")

    def _processar_medidas(self, numero: str, mensagem: str) -> None:
        """Processa mensagens contendo medidas para orçamento"""
        try:
            # Extrair medidas da mensagem
            medidas = extrair_medidas(mensagem)
            if not medidas:
                self.whatsapp.enviar_mensagem_texto(
                    numero, 
                    "Por favor, informe as medidas no formato: largura x altura (ex: 3x2)"
                )
                return

            # Calcular orçamento
            tipo_portao = identificar_tipo_portao(mensagem)
            valor = calcular_orcamento(tipo_portao, medidas)

            # Salvar orçamento
            self.db.adicionar_orcamento(numero, tipo_portao, medidas, valor)

            # Enviar orçamento
            detalhes = {
                "tipo_portao": tipo_portao,
                "medidas": medidas,
                "valor": valor
            }
            mensagem_orcamento = formatar_mensagem_orcamento(detalhes)
            self.whatsapp.enviar_mensagem_texto(numero, mensagem_orcamento)

        except Exception as e:
            log_message(agent_logger, "error", f"Erro ao processar medidas: {str(e)}")

    def _processar_agendamento(self, numero: str, mensagem: str) -> None:
        """Processa solicitações de agendamento"""
        try:
            # Extrair data e horário da mensagem
            data, horario = extrair_data_horario(mensagem)
            if not data or not horario:
                self.whatsapp.enviar_mensagem_texto(
                    numero,
                    "Por favor, informe a data e horário desejados (ex: 25/12/2023 14:30)"
                )
                return

            # Agendar visita
            if self.db.agendar_visita(numero, data, horario):
                mensagem_visita = formatar_mensagem_visita(data, horario)
                self.whatsapp.enviar_mensagem_texto(numero, mensagem_visita)

        except Exception as e:
            log_message(agent_logger, "error", f"Erro ao processar agendamento: {str(e)}") 