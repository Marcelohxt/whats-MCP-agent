from django.contrib import admin
from .models import Servico, ProjetoPorfolio, Depoimento, InformacaoContato

@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'ordem']
    list_editable = ['ordem']
    search_fields = ['titulo', 'descricao']

@admin.register(ProjetoPorfolio)
class ProjetoPortfolioAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'data_realizacao', 'ordem']
    list_editable = ['ordem']
    search_fields = ['titulo', 'descricao']
    date_hierarchy = 'data_realizacao'

@admin.register(Depoimento)
class DepoimentoAdmin(admin.ModelAdmin):
    list_display = ['nome_cliente', 'cidade', 'ativo']
    list_editable = ['ativo']
    search_fields = ['nome_cliente', 'texto']
    list_filter = ['ativo']

@admin.register(InformacaoContato)
class InformacaoContatoAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Limita a criação de apenas uma instância
        if self.model.objects.exists():
            return False
        return True
