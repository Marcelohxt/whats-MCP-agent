from django.db import models

# Create your models here.

class Servico(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    icone = models.CharField(max_length=50)  # classe do Font Awesome
    ordem = models.IntegerField(default=0)

    class Meta:
        ordering = ['ordem']
        verbose_name = 'Serviço'
        verbose_name_plural = 'Serviços'

    def __str__(self):
        return self.titulo

class ProjetoPorfolio(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    imagem = models.ImageField(upload_to='portfolio/')
    data_realizacao = models.DateField()
    ordem = models.IntegerField(default=0)

    class Meta:
        ordering = ['ordem']
        verbose_name = 'Projeto do Portfólio'
        verbose_name_plural = 'Projetos do Portfólio'

    def __str__(self):
        return self.titulo

class Depoimento(models.Model):
    nome_cliente = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100, blank=True)
    foto = models.ImageField(upload_to='depoimentos/', blank=True)
    texto = models.TextField()
    cidade = models.CharField(max_length=100)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f"Depoimento de {self.nome_cliente}"

class InformacaoContato(models.Model):
    endereco = models.TextField()
    telefone = models.CharField(max_length=20)
    whatsapp = models.CharField(max_length=20)
    email = models.EmailField()
    horario_funcionamento = models.TextField()
    mapa_embed = models.TextField(help_text='Código de incorporação do Google Maps', blank=True)

    class Meta:
        verbose_name = 'Informação de Contato'
        verbose_name_plural = 'Informações de Contato'

    def __str__(self):
        return "Informações de Contato"
