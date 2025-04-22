import requests
from django.conf import settings
from typing import Dict, Any, Optional

class SiengeClient:
    def __init__(self):
        self.base_url = settings.SIENGE_API_URL
        self.api_key = settings.SIENGE_API_KEY
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        })

    def get_purchase_requests(self, params: Optional[Dict[str, Any]] = None) -> Dict:
        """Obtém solicitações de compra do Sienge."""
        endpoint = f"{self.base_url}/purchasing/purchase-requests"
        response = self.session.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()

    def get_purchase_orders(self, params: Optional[Dict[str, Any]] = None) -> Dict:
        """Obtém pedidos de compra do Sienge."""
        endpoint = f"{self.base_url}/purchasing/purchase-orders"
        response = self.session.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()

    def get_budget_items(self, params: Optional[Dict[str, Any]] = None) -> Dict:
        """Obtém itens do orçamento do Sienge."""
        endpoint = f"{self.base_url}/construction/budget-items"
        response = self.session.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()

    def get_stock_items(self, params: Optional[Dict[str, Any]] = None) -> Dict:
        """Obtém itens do estoque do Sienge."""
        endpoint = f"{self.base_url}/stock/items"
        response = self.session.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()