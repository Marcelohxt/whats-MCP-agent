from typing import Dict, List, Optional
import json
import os
from datetime import datetime

class ClientesDB:
    def __init__(self, arquivo_db: str = "clientes.json"):
        self.arquivo_db = arquivo_db
        self.clientes = self._carregar_db()

    def _carregar_db(self) -> Dict:
        """Carrega o banco de dados de clientes do arquivo JSON"""
        if os.path.exists(self.arquivo_db):
            with open(self.arquivo_db, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _salvar_db(self):
        """Salva o banco de dados de clientes no arquivo JSON"""
        with open(self.arquivo_db, 'w', encoding='utf-8') as f:
            json.dump(self.clientes, f, ensure_ascii=False, indent=4)

    def adicionar_cliente(self, numero: str, nome: str, endereco: str) -> bool:
        """Adiciona um novo cliente ao banco de dados"""
        if numero in self.clientes:
            return False

        self.clientes[numero] = {
            "nome": nome,
            "endereco": endereco,
            "data_cadastro": datetime.now().isoformat(),
            "orcamentos": [],
            "visitas_agendadas": []
        }
        self._salvar_db()
        return True

    def adicionar_orcamento(self, numero: str, tipo_portao: str, medidas: Dict, valor: float) -> bool:
        """Adiciona um orçamento ao histórico do cliente"""
        if numero not in self.clientes:
            return False

        orcamento = {
            "tipo_portao": tipo_portao,
            "medidas": medidas,
            "valor": valor,
            "data": datetime.now().isoformat()
        }

        self.clientes[numero]["orcamentos"].append(orcamento)
        self._salvar_db()
        return True

    def agendar_visita(self, numero: str, data: str, horario: str) -> bool:
        """Agenda uma visita técnica para o cliente"""
        if numero not in self.clientes:
            return False

        visita = {
            "data": data,
            "horario": horario,
            "status": "agendada"
        }

        self.clientes[numero]["visitas_agendadas"].append(visita)
        self._salvar_db()
        return True

    def get_cliente(self, numero: str) -> Optional[Dict]:
        """Retorna as informações de um cliente específico"""
        return self.clientes.get(numero)

    def get_historico_orcamentos(self, numero: str) -> List[Dict]:
        """Retorna o histórico de orçamentos de um cliente"""
        if numero not in self.clientes:
            return []
        return self.clientes[numero]["orcamentos"]

    def get_visitas_agendadas(self, numero: str) -> List[Dict]:
        """Retorna as visitas agendadas de um cliente"""
        if numero not in self.clientes:
            return []
        return self.clientes[numero]["visitas_agendadas"] 