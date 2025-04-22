from django.views.generic import TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from .services.price_scraper import PriceScraperService
from .forms import MaterialQuoteForm, BulkQuoteForm
import json
import asyncio
from datetime import datetime, timedelta
import random

class MarketIntelligenceView(TemplateView):
    template_name = 'market_intelligence/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sample_news'] = self.get_sample_news()
        context['price_trends'] = self.get_price_trends()
        return context

    def get_price_trends(self):
        # Dados de exemplo para tendências de preços
        materials = ['Cimento', 'Areia', 'Brita', 'Tijolo', 'Aço']
        trends = []
        
        base_date = datetime.now()
        for material in materials:
            price_history = []
            base_price = random.uniform(50, 500)
            
            for i in range(7):
                date = base_date - timedelta(days=i)
                variation = random.uniform(-5, 5)
                price = base_price + variation
                price_history.append({
                    'date': date.strftime('%d/%m/%Y'),
                    'price': round(price, 2)
                })
            
            trends.append({
                'material': material,
                'history': price_history,
                'current_price': round(price_history[0]['price'], 2),
                'variation': round(((price_history[0]['price'] - price_history[-1]['price']) / price_history[-1]['price']) * 100, 2)
            })
        
        return trends

    def get_sample_news(self):
        # Dados de exemplo para notícias do mercado
        base_date = datetime.now()
        news_list = [
            {
                'title': 'Aumento no preço do aço impacta construção civil',
                'date': (base_date - timedelta(days=1)).strftime('%d/%m/%Y'),
                'source': 'Construção Mercado',
                'summary': 'Preços do aço registram aumento de 15% no último mês devido à demanda global.'
            },
            {
                'title': 'Novos materiais sustentáveis ganham mercado',
                'date': (base_date - timedelta(days=2)).strftime('%d/%m/%Y'),
                'source': 'Revista Construir',
                'summary': 'Materiais eco-friendly apresentam crescimento de 25% nas vendas do setor.'
            },
            {
                'title': 'Cimento tem queda de preço em março',
                'date': (base_date - timedelta(days=3)).strftime('%d/%m/%Y'),
                'source': 'Portal Construção',
                'summary': 'Preço do cimento registra queda de 5% devido ao aumento da oferta.'
            }
        ]
        return news_list

    def get(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            data = {
                'price_trends': self.get_price_trends(),
                'news': self.get_sample_news()
            }
            return JsonResponse(data)
        return super().get(request, *args, **kwargs)

class QuoteSearchView(FormView):
    template_name = 'market_intelligence/quote_search.html'
    form_class = MaterialQuoteForm
    success_url = reverse_lazy('market_intelligence:quote_search')

    def form_valid(self, form):
        try:
            material = form.cleaned_data['name']
            scraper = PriceScraperService()
            results = scraper.search_material(material)
            
            if form.cleaned_data.get('generate_report'):
                filename = scraper.generate_report(
                    results, 
                    form.cleaned_data['report_format']
                )
                return JsonResponse({
                    'success': True,
                    'results': results,
                    'report_url': f'/media/results/{filename}'
                })
            
            return JsonResponse({
                'success': True,
                'results': results
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })

class BulkQuoteView(FormView):
    template_name = 'market_intelligence/bulk_quote.html'
    form_class = BulkQuoteForm
    success_url = reverse_lazy('market_intelligence:bulk_quote')

    def form_valid(self, form):
        try:
            file = form.cleaned_data['file']
            scraper = PriceScraperService()
            results = scraper.process_bulk_file(file.temporary_file_path())
            filename = scraper.generate_report(
                results.to_dict('records'),
                form.cleaned_data['report_format']
            )
            
            return JsonResponse({
                'success': True,
                'report_url': f'/media/results/{filename}'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }) 