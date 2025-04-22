import json
import os
from typing import Dict, Any, Optional, List
from datetime import datetime
from logger import agent_logger, log_message
import shutil

class DataPersistence:
    def __init__(self, base_dir: str = "data"):
        self.base_dir = base_dir
        self._criar_estrutura_diretorios()

    def _criar_estrutura_diretorios(self):
        """Cria a estrutura de diretórios para armazenar os dados"""
        diretorios = [
            os.path.join(self.base_dir, "clientes"),
            os.path.join(self.base_dir, "orcamentos"),
            os.path.join(self.base_dir, "agendamentos")
        ]
        
        for diretorio in diretorios:
            os.makedirs(diretorio, exist_ok=True)

    def _get_caminho_arquivo(self, tipo: str, id: str) -> str:
        """Retorna o caminho do arquivo para um determinado tipo e ID"""
        return os.path.join(self.base_dir, tipo, f"{id}.json")

    def salvar_dados(self, tipo: str, id: str, dados: Dict[str, Any]) -> bool:
        """Salva dados em um arquivo JSON"""
        try:
            caminho = self._get_caminho_arquivo(tipo, id)
            
            # Adicionar metadados
            dados["_ultima_atualizacao"] = datetime.now().isoformat()
            
            with open(caminho, 'w', encoding='utf-8') as f:
                json.dump(dados, f, ensure_ascii=False, indent=4)
            
            log_message(agent_logger, "info", f"Dados salvos em {caminho}")
            return True

        except Exception as e:
            log_message(agent_logger, "error", f"Erro ao salvar dados: {str(e)}")
            return False

    def carregar_dados(self, tipo: str, id: str) -> Optional[Dict[str, Any]]:
        """Carrega dados de um arquivo JSON"""
        try:
            caminho = self._get_caminho_arquivo(tipo, id)
            
            if not os.path.exists(caminho):
                return None
            
            with open(caminho, 'r', encoding='utf-8') as f:
                dados = json.load(f)
            
            return dados

        except Exception as e:
            log_message(agent_logger, "error", f"Erro ao carregar dados: {str(e)}")
            return None

    def listar_ids(self, tipo: str) -> List[str]:
        """Lista todos os IDs disponíveis para um tipo de dado"""
        try:
            diretorio = os.path.join(self.base_dir, tipo)
            if not os.path.exists(diretorio):
                return []

            ids = []
            for arquivo in os.listdir(diretorio):
                if arquivo.endswith('.json'):
                    ids.append(arquivo[:-5])  # Remove a extensão .json

            return ids

        except Exception as e:
            log_message(agent_logger, "error", f"Erro ao listar IDs: {str(e)}")
            return []

    def remover_dados(self, tipo: str, id: str) -> bool:
        """Remove um arquivo de dados"""
        try:
            caminho = self._get_caminho_arquivo(tipo, id)
            
            if os.path.exists(caminho):
                os.remove(caminho)
                log_message(agent_logger, "info", f"Dados removidos: {caminho}")
                return True
            
            return False

        except Exception as e:
            log_message(agent_logger, "error", f"Erro ao remover dados: {str(e)}")
            return False

    def backup_dados(self) -> bool:
        """Cria um backup dos dados"""
        try:
            data_hora = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_dir = f"backup_{data_hora}"
            
            # Criar diretório de backup
            os.makedirs(backup_dir, exist_ok=True)
            
            # Copiar todos os arquivos
            for tipo in ["clientes", "orcamentos", "agendamentos"]:
                origem = os.path.join(self.base_dir, tipo)
                destino = os.path.join(backup_dir, tipo)
                
                if os.path.exists(origem):
                    shutil.copytree(origem, destino)
            
            log_message(agent_logger, "info", f"Backup criado em {backup_dir}")
            return True

        except Exception as e:
            log_message(agent_logger, "error", f"Erro ao criar backup: {str(e)}")
            return False 