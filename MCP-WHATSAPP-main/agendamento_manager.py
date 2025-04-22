from typing import Dict, List, Optional
from datetime import datetime, timedelta
from logger import agent_logger, log_message

class AgendamentoManager:
    def __init__(self):
        self.agendamentos = {}  # {data: {horario: {cliente: info}}}
        self.horarios_disponiveis = self._gerar_horarios_disponiveis()

    def _gerar_horarios_disponiveis(self) -> List[str]:
        """Gera a lista de horários disponíveis para agendamento"""
        horarios = []
        hora_inicio = 8  # 8:00
        hora_fim = 18    # 18:00
        
        for hora in range(hora_inicio, hora_fim):
            horarios.append(f"{hora:02d}:00")
            horarios.append(f"{hora:02d}:30")
        
        return horarios

    def verificar_disponibilidade(self, data: str, horario: str) -> bool:
        """Verifica se um horário está disponível para agendamento"""
        try:
            # Verificar se a data está no futuro
            data_agendamento = datetime.strptime(f"{data} {horario}", "%d/%m/%Y %H:%M")
            if data_agendamento < datetime.now():
                return False

            # Verificar se o horário está disponível
            if data not in self.agendamentos:
                return True

            return horario not in self.agendamentos[data]

        except Exception as e:
            log_message(agent_logger, "error", f"Erro ao verificar disponibilidade: {str(e)}")
            return False

    def agendar_visita(self, cliente: str, data: str, horario: str, info: Dict) -> bool:
        """Agenda uma visita técnica"""
        try:
            if not self.verificar_disponibilidade(data, horario):
                return False

            if data not in self.agendamentos:
                self.agendamentos[data] = {}

            self.agendamentos[data][horario] = {
                "cliente": cliente,
                "info": info,
                "status": "agendada",
                "data_criacao": datetime.now().isoformat()
            }

            log_message(agent_logger, "info", f"Visita agendada para {cliente} em {data} às {horario}")
            return True

        except Exception as e:
            log_message(agent_logger, "error", f"Erro ao agendar visita: {str(e)}")
            return False

    def cancelar_visita(self, data: str, horario: str) -> bool:
        """Cancela uma visita agendada"""
        try:
            if data in self.agendamentos and horario in self.agendamentos[data]:
                del self.agendamentos[data][horario]
                log_message(agent_logger, "info", f"Visita cancelada para {data} às {horario}")
                return True
            return False

        except Exception as e:
            log_message(agent_logger, "error", f"Erro ao cancelar visita: {str(e)}")
            return False

    def listar_visitas_dia(self, data: str) -> List[Dict]:
        """Lista todas as visitas agendadas para um dia específico"""
        try:
            if data not in self.agendamentos:
                return []

            visitas = []
            for horario, info in self.agendamentos[data].items():
                visitas.append({
                    "horario": horario,
                    "cliente": info["cliente"],
                    "status": info["status"]
                })

            return sorted(visitas, key=lambda x: x["horario"])

        except Exception as e:
            log_message(agent_logger, "error", f"Erro ao listar visitas: {str(e)}")
            return []

    def atualizar_status_visita(self, data: str, horario: str, novo_status: str) -> bool:
        """Atualiza o status de uma visita agendada"""
        try:
            if data in self.agendamentos and horario in self.agendamentos[data]:
                self.agendamentos[data][horario]["status"] = novo_status
                log_message(agent_logger, "info", 
                          f"Status da visita atualizado para {novo_status} em {data} às {horario}")
                return True
            return False

        except Exception as e:
            log_message(agent_logger, "error", f"Erro ao atualizar status da visita: {str(e)}")
            return False 