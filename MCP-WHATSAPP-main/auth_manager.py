import os
import jwt
from datetime import datetime, timedelta
from typing import Dict, Optional, List
from logger import agent_logger, log_message

class AuthManager:
    def __init__(self):
        self.secret_key = os.getenv("JWT_SECRET_KEY", "sua_chave_secreta_aqui")
        self.token_expiration = timedelta(hours=24)
        self.tokens = {}  # Armazenamento temporário de tokens

    def gerar_token(self, user_id: str, roles: List[str]) -> str:
        """Gera um token JWT para um usuário"""
        try:
            payload = {
                "user_id": user_id,
                "roles": roles,
                "exp": datetime.utcnow() + self.token_expiration
            }
            
            token = jwt.encode(payload, self.secret_key, algorithm="HS256")
            self.tokens[token] = payload
            
            log_message(agent_logger, "info", f"Token gerado para usuário {user_id}")
            return token

        except Exception as e:
            log_message(agent_logger, "error", f"Erro ao gerar token: {str(e)}")
            return ""

    def verificar_token(self, token: str) -> Optional[Dict]:
        """Verifica se um token é válido"""
        try:
            if token not in self.tokens:
                return None

            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            
            # Verificar se o token expirou
            if datetime.utcnow() > datetime.fromtimestamp(payload["exp"]):
                del self.tokens[token]
                return None
            
            return payload

        except jwt.ExpiredSignatureError:
            log_message(agent_logger, "warning", "Token expirado")
            return None
        except jwt.InvalidTokenError:
            log_message(agent_logger, "warning", "Token inválido")
            return None
        except Exception as e:
            log_message(agent_logger, "error", f"Erro ao verificar token: {str(e)}")
            return None

    def verificar_permissao(self, token: str, role_necessaria: str) -> bool:
        """Verifica se um usuário tem uma permissão específica"""
        try:
            payload = self.verificar_token(token)
            if not payload:
                return False

            return role_necessaria in payload["roles"]

        except Exception as e:
            log_message(agent_logger, "error", f"Erro ao verificar permissão: {str(e)}")
            return False

    def revogar_token(self, token: str) -> bool:
        """Revoga um token"""
        try:
            if token in self.tokens:
                del self.tokens[token]
                log_message(agent_logger, "info", "Token revogado")
                return True
            return False

        except Exception as e:
            log_message(agent_logger, "error", f"Erro ao revogar token: {str(e)}")
            return False

    def limpar_tokens_expirados(self):
        """Remove tokens expirados do armazenamento"""
        try:
            tokens_para_remover = []
            for token, payload in self.tokens.items():
                if datetime.utcnow() > datetime.fromtimestamp(payload["exp"]):
                    tokens_para_remover.append(token)

            for token in tokens_para_remover:
                del self.tokens[token]

            if tokens_para_remover:
                log_message(agent_logger, "info", 
                          f"{len(tokens_para_remover)} tokens expirados removidos")

        except Exception as e:
            log_message(agent_logger, "error", f"Erro ao limpar tokens expirados: {str(e)}") 