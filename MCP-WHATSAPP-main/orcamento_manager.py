from typing import Dict, List, Optional
from datetime import datetime
from logger import agent_logger, log_message
from portoes_data import PORTÕES, calcular_orcamento

class OrcamentoManager:
    def __init__(self):
        self.orcamentos = {}  # {cliente: [orcamentos]}

    def criar_orcamento(self, cliente: str, tipo_portao: str, medidas: Dict) -> Optional[Dict]:
        """Cria um novo orçamento"""
        try:
            # Verificar se o tipo de portão existe
            if tipo_portao not in PORTÕES:
                log_message(agent_logger, "error", f"Tipo de portão inválido: {tipo_portao}")
                return None

            # Calcular valor
            valor = calcular_orcamento(tipo_portao, medidas)

            # Criar orçamento
            orcamento = {
                "tipo_portao": tipo_portao,
                "medidas": medidas,
                "valor": valor,
                "data_criacao": datetime.now().isoformat(),
                "status": "pendente"
            }

            # Armazenar orçamento
            if cliente not in self.orcamentos:
                self.orcamentos[cliente] = []

            self.orcamentos[cliente].append(orcamento)
            log_message(agent_logger, "info", f"Orçamento criado para {cliente}")

            return orcamento

        except Exception as e:
            log_message(agent_logger, "error", f"Erro ao criar orçamento: {str(e)}")
            return None

    def listar_orcamentos_cliente(self, cliente: str) -> List[Dict]:
        """Lista todos os orçamentos de um cliente"""
        try:
            return self.orcamentos.get(cliente, [])

        except Exception as e:
            log_message(agent_logger, "error", f"Erro ao listar orçamentos: {str(e)}")
            return []

    def atualizar_status_orcamento(self, cliente: str, indice: int, novo_status: str) -> bool:
        """Atualiza o status de um orçamento"""
        try:
            if cliente in self.orcamentos and 0 <= indice < len(self.orcamentos[cliente]):
                self.orcamentos[cliente][indice]["status"] = novo_status
                log_message(agent_logger, "info", 
                          f"Status do orçamento atualizado para {novo_status}")
                return True
            return False

        except Exception as e:
            log_message(agent_logger, "error", f"Erro ao atualizar status do orçamento: {str(e)}")
            return False

    def get_orcamento_atual(self, cliente: str) -> Optional[Dict]:
        """Retorna o orçamento mais recente de um cliente"""
        try:
            if cliente in self.orcamentos and self.orcamentos[cliente]:
                return self.orcamentos[cliente][-1]
            return None

        except Exception as e:
            log_message(agent_logger, "error", f"Erro ao obter orçamento atual: {str(e)}")
            return None

    def formatar_orcamento(self, orcamento: Dict) -> str:
        """Formata um orçamento em uma mensagem legível"""
        try:
            tipo_portao = PORTÕES[orcamento["tipo_portao"]]["nome"]
            medidas = orcamento["medidas"]
            valor = orcamento["valor"]

            return f"""*Orçamento para Portão*

Tipo: {tipo_portao}
Medidas: {medidas['largura']}m x {medidas['altura']}m
Valor: R$ {valor:.2f}

Para agendar uma visita técnica, responda com 'AGENDAR'."""

        except Exception as e:
            log_message(agent_logger, "error", f"Erro ao formatar orçamento: {str(e)}")
            return "Erro ao formatar orçamento" 