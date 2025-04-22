import os
import shutil
from typing import List, Optional
from config import DIRETORIOS
from logger import agent_logger, log_message

class ImageManager:
    def __init__(self):
        self.base_dir = DIRETORIOS["imagens"]
        self._criar_estrutura_diretorios()

    def _criar_estrutura_diretorios(self):
        """Cria a estrutura de diretórios para armazenar as imagens"""
        tipos_portoes = ["ferro", "aluminio", "aco"]
        
        for tipo in tipos_portoes:
            diretorio = os.path.join(self.base_dir, tipo)
            os.makedirs(diretorio, exist_ok=True)

    def adicionar_imagem(self, tipo_portao: str, caminho_imagem: str) -> Optional[str]:
        """Adiciona uma nova imagem para um tipo de portão"""
        try:
            if not os.path.exists(caminho_imagem):
                log_message(agent_logger, "error", f"Arquivo de imagem não encontrado: {caminho_imagem}")
                return None

            # Criar nome único para o arquivo
            nome_arquivo = f"portao_{len(self.listar_imagens(tipo_portao)) + 1}.jpg"
            caminho_destino = os.path.join(self.base_dir, tipo_portao, nome_arquivo)

            # Copiar a imagem
            shutil.copy2(caminho_imagem, caminho_destino)
            
            log_message(agent_logger, "info", f"Imagem adicionada: {caminho_destino}")
            return caminho_destino

        except Exception as e:
            log_message(agent_logger, "error", f"Erro ao adicionar imagem: {str(e)}")
            return None

    def listar_imagens(self, tipo_portao: str) -> List[str]:
        """Lista todas as imagens disponíveis para um tipo de portão"""
        try:
            diretorio = os.path.join(self.base_dir, tipo_portao)
            if not os.path.exists(diretorio):
                return []

            imagens = []
            for arquivo in os.listdir(diretorio):
                if arquivo.lower().endswith(('.jpg', '.jpeg', '.png')):
                    imagens.append(os.path.join(diretorio, arquivo))

            return imagens

        except Exception as e:
            log_message(agent_logger, "error", f"Erro ao listar imagens: {str(e)}")
            return []

    def remover_imagem(self, caminho_imagem: str) -> bool:
        """Remove uma imagem específica"""
        try:
            if os.path.exists(caminho_imagem):
                os.remove(caminho_imagem)
                log_message(agent_logger, "info", f"Imagem removida: {caminho_imagem}")
                return True
            return False

        except Exception as e:
            log_message(agent_logger, "error", f"Erro ao remover imagem: {str(e)}")
            return False

    def obter_url_imagem(self, caminho_imagem: str) -> Optional[str]:
        """Converte o caminho local da imagem em uma URL acessível"""
        try:
            if not os.path.exists(caminho_imagem):
                return None

            # Aqui você implementaria a lógica para fazer upload da imagem
            # para um serviço de armazenamento em nuvem e retornar a URL
            # Por enquanto, retornamos o caminho local
            return caminho_imagem

        except Exception as e:
            log_message(agent_logger, "error", f"Erro ao obter URL da imagem: {str(e)}")
            return None 