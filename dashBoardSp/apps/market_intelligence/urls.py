from django.urls import path
from . import views

app_name = 'market_intelligence'

urlpatterns = [
    path('', views.MarketIntelligenceView.as_view(), name='dashboard'),
    path('quote/', views.QuoteSearchView.as_view(), name='quote_search'),
    path('bulk-quote/', views.BulkQuoteView.as_view(), name='bulk_quote'),
] 