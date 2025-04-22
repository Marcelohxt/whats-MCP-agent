from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='index'),
    path('suprimentos/', views.SuprimentosView.as_view(), name='suprimentos'),
    path('orcamentos/', views.OrcamentosView.as_view(), name='orcamentos'),
] 