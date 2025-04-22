from typing import Dict, List, Optional
from datetime import datetime, timedelta
from logger import agent_logger, log_message
from config import MAX_REQUESTS_PER_MINUTE, RATE_LIMIT_WINDOW

class RateLimiter:
    def __init__(self, max_requests: int = MAX_REQUESTS_PER_MINUTE, time_window: int = RATE_LIMIT_WINDOW):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests: Dict[str, List[datetime]] = {}

    def is_allowed(self, client_id: str) -> tuple[bool, Optional[int]]:
        """
        Verifica se um cliente pode fazer uma requisição.
        Retorna uma tupla com (permitido, tempo_restante)
        """
        try:
            now = datetime.now()
            
            # Limpa requisições antigas
            if client_id in self.requests:
                self.requests[client_id] = [
                    req_time for req_time in self.requests[client_id]
                    if (now - req_time).total_seconds() <= self.time_window
                ]
            
            # Adiciona nova requisição
            if client_id not in self.requests:
                self.requests[client_id] = []
            
            # Verifica se excedeu o limite
            if len(self.requests[client_id]) >= self.max_requests:
                # Calcula o tempo restante até a próxima requisição permitida
                oldest_request = self.requests[client_id][0]
                time_remaining = int((oldest_request + timedelta(seconds=self.time_window) - now).total_seconds())
                return False, max(0, time_remaining)
            
            # Registra a nova requisição
            self.requests[client_id].append(now)
            return True, None

        except Exception as e:
            log_message(agent_logger, "error", f"Erro no rate limiter: {str(e)}")
            return True, None  # Em caso de erro, permitir a requisição

    def get_remaining_requests(self, client_id: str) -> int:
        """
        Retorna o número de requisições restantes para um cliente.
        """
        try:
            if client_id not in self.requests:
                return self.max_requests
            
            now = datetime.now()
            self.requests[client_id] = [
                req_time for req_time in self.requests[client_id]
                if (now - req_time).total_seconds() <= self.time_window
            ]
            
            return self.max_requests - len(self.requests[client_id])

        except Exception as e:
            log_message(agent_logger, "error", 
                      f"Erro ao obter requisições restantes: {str(e)}")
            return self.max_requests

    def reset(self, client_id: str = None):
        """Reseta o contador de requisições"""
        try:
            if client_id:
                if client_id in self.requests:
                    del self.requests[client_id]
            else:
                self.requests.clear()
            
            log_message(agent_logger, "info", "Rate limiter resetado")

        except Exception as e:
            log_message(agent_logger, "error", f"Erro ao resetar rate limiter: {str(e)}")

    def get_wait_time(self, client_id: str) -> timedelta:
        """Retorna o tempo de espera necessário para fazer uma nova requisição"""
        try:
            if client_id not in self.requests or not self.requests[client_id]:
                return timedelta(seconds=0)
            
            now = datetime.now()
            oldest_request = min(self.requests[client_id])
            
            if now - oldest_request >= self.time_window:
                return timedelta(seconds=0)
            
            return self.time_window - (now - oldest_request)

        except Exception as e:
            log_message(agent_logger, "error", f"Erro ao obter tempo de espera: {str(e)}")
            return timedelta(seconds=0) 