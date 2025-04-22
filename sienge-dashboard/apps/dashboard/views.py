from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
import requests
import random
from datetime import datetime, timedelta

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Aqui você pode adicionar dados para o dashboard
        return context

class SuprimentosView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/suprimentos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Simulando dados (em produção, isso viria da API do Sienge)
        solicitacoes = [
            {
                'numero': f'SOL-{random.randint(1000, 9999)}',
                'data': (datetime.now() - timedelta(days=random.randint(0, 30))).strftime('%d/%m/%Y'),
                'status': random.choice(['Pendente', 'Em Análise', 'Aprovado', 'Rejeitado']),
                'valor': random.uniform(1000, 50000)
            } for _ in range(5)
        ]

        context.update({
            'solicitacoes_pendentes': random.randint(5, 15),
            'pedidos_andamento': random.randint(3, 10),
            'cotacoes_abertas': random.randint(2, 8),
            'total_estoque': random.uniform(100000, 500000),
            'ultimas_solicitacoes': solicitacoes
        })
        
        return context

class OrcamentosView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/orcamentos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Aqui você pode adicionar dados específicos de orçamentos
        return context 