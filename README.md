# WhatsApp Simulator - Sistema de Atendimento Automatizado

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![Status](https://img.shields.io/badge/status-production--ready-green)

## 📱 Sobre o Projeto

![Interface do Sistema](https://github.com/user-attachments/assets/5f94e39d-60a4-4851-b59f-9b8301da9e65)

O WhatsApp Simulator é um sistema avançado de atendimento automatizado que simula a interface e funcionalidades do WhatsApp. Desenvolvido para empresas que desejam automatizar e melhorar seu atendimento ao cliente, o sistema oferece uma experiência familiar aos usuários enquanto proporciona ferramentas poderosas de automação.

### 🌟 Desenvolvedor
- **Nome:** Marcelo Henrique
- **Email:** marcelo_hxt@hotmail.com
- **Tel:** 55-11-910521048
- **LinkedIn:** 
- **GitHub:**
  

## 🚀 Funcionalidades

### Interface do Usuário
- 💬 Chat em tempo real
- 🎤 Gravação e envio de áudio
- 📷 Envio de imagens
- 🔄 Status de conexão em tempo real
- 🗑️ Gerenciamento de conversas

### Processamento de Mídia
- 🎵 Otimização automática de áudio
  - Formato MP3
  - Taxa de amostragem: 16kHz
  - Áudio mono
  - Limite de 30 segundos
  - Compressão inteligente
- 🖼️ Otimização de imagens
  - Redimensionamento automático
  - Compressão JPEG
  - Qualidade adaptativa
  - Suporte a múltiplos formatos

### Comunicação
- 🔌 API Webhook
- ⚡ Comunicação assíncrona
- 🔒 Tratamento seguro de dados
- 📊 Monitoramento de status

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+**
- **Tkinter** - Interface gráfica
- **Requests** - Comunicação HTTP
- **SoundDevice** - Processamento de áudio
- **Pillow** - Processamento de imagens
- **PyDub** - Manipulação de áudio
- **NumPy** - Processamento numérico
- **Base64** - Codificação de mídia

## ⚙️ Instalação

1. **Clone o repositório**
```bash
git clone [[URL_DO_REPOSITÓRIO](https://github.com/Marcelohxt/whats-MCP-agent.git)]
cd MCP-WHATSAPP-main
```

2. **Crie um ambiente virtual**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

## 🚦 Uso

![Exemplo de Uso](https://github.com/user-attachments/assets/873561aa-c763-47db-a283-06f027256de0)

## ⚙️ Configuração

### 1. Meta Developer Portal

1. Acesse [Meta Developers](https://developers.facebook.com/)
2. Crie um novo app ou use um existente
3. Adicione o produto "WhatsApp" ao seu app
4. Configure o webhook
5. Obtenha as credenciais necessárias

### 2. Variáveis de Ambiente

Edite o arquivo `.env` com suas configurações:

```env
WHATSAPP_TOKEN=seu_token_aqui
VERIFY_TOKEN=seu_token_de_verificacao
```

### 3. Inicialização

1. **Inicie o servidor**
```bash
python server.py
```

2. **Execute o simulador**
```bash
python whatsapp_simulator.py
```

3. **Configure o Postman (para testes)**
- Importe a coleção de endpoints
- Configure as variáveis de ambiente
- Execute os testes disponíveis

## 📡 API Endpoints

### POST /webhook
```json
{
    "messages": [
        {
            "from": "5511930779357",
            "type": "text|audio|image",
            "body": "conteúdo_da_mensagem",
            "filename": "nome_do_arquivo"  // para mídia
        }
    ]
}
```

### GET /api/status
- Retorna o status atual do servidor

## 🔧 Configurações do Sistema

### Configurações do Servidor
```python
HOST = "localhost"
PORT = 8000
MAX_AUDIO_DURATION = 30  # segundos
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
```

### Configurações de Mídia
```python
AUDIO_SAMPLE_RATE = 16000
AUDIO_CHANNELS = 1
IMAGE_MAX_SIZE = (800, 800)
IMAGE_QUALITY = 85
```

## 🎯 Casos de Uso

- **Clínicas e Consultórios**
  - Agendamento automatizado
  - Confirmação de consultas
  - Envio de resultados

- **Comércio**
  - Atendimento ao cliente
  - Catálogo de produtos
  - Status de pedidos

- **Serviços**
  - Orçamentos automáticos
  - Agendamento de serviços
  - Suporte técnico

## 📈 Roadmap

- [ ] Integração com IA para respostas automáticas
- [ ] Painel administrativo web
- [ ] Análise de sentimentos
- [ ] Relatórios e métricas
- [ ] Integração com CRM
- [ ] Suporte a múltiplos idiomas

## 🤝 Contribuição

Contribuições são bem-vindas! Para contribuir:

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 📞 Suporte

Para suporte e dúvidas, entre em contato:
- Email: marcelo_hxt@hotmail.com
- Issues: [GitHub Issues](link_para_issues)

## 🙏 Agradecimentos

- Equipe de desenvolvimento
- Contribuidores
- Usuários e testadores

---
Desenvolvido com ❤️ por Marcelo Henrique

[⬆ Voltar ao topo](#whatsapp-simulator---sistema-de-atendimento-automatizado) 
