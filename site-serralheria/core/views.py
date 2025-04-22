from django.shortcuts import render
from .models import Servico, ProjetoPorfolio, Depoimento, InformacaoContato

def index(request):
    context = {
        'servicos': Servico.objects.all(),
        'projetos': ProjetoPorfolio.objects.all(),
        'depoimentos': Depoimento.objects.filter(ativo=True),
        'contato': InformacaoContato.objects.first()
    }
    return render(request, 'core/index.html', context)
