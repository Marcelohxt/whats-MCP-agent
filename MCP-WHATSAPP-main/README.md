# WhatsApp Webhook Server

Um servidor webhook em Python usando FastAPI para integração com a API do WhatsApp Business. Este projeto permite receber e responder mensagens do WhatsApp automaticamente com comandos personalizados.

![Banner do Projeto](./images/banner.png)

## 📋 Índice

- [Funcionalidades](#-funcionalidades)
- [Requisitos](#-requisitos)
- [Instalação](#-instalação)
- [Configuração](#-configuração)
- [Uso](#-uso)
- [Comandos Disponíveis](#-comandos-disponíveis)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Testes](#-testes)
- [Contribuição](#-contribuição)
- [Licença](#-licença)

## ✨ Funcionalidades

- Recebimento de mensagens do WhatsApp em tempo real
- Processamento automático de comandos
- Respostas automáticas personalizadas
- Verificação de webhook integrada
- Comandos úteis pré-configurados (hora, data, ajuda)
- Interface de logs detalhada

![Demo dos Comandos](./images/demo-commands.png)

## 📦 Requisitos

- Python 3.8+
- Conta no WhatsApp Business
- Conta no Meta Developer Portal
- Servidor com acesso HTTPS (para produção)

## 🚀 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/whatsapp-webhook.git
cd whatsapp-webhook
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure as variáveis de ambiente:
```bash
cp .env.example .env
```

![Configuração do Ambiente](./images/env-setup.png)

## ⚙️ Configuração

### 1. Meta Developer Portal

1. Acesse [Meta Developers](https://developers.facebook.com/)
2. Crie um novo app ou use um existente
3. Adicione o produto "WhatsApp" ao seu app
4. Configure o webhook
5. Obtenha as credenciais necessárias

![Configuração Meta Developer](./images/meta-dev-setup.png)

### 2. Variáveis de Ambiente

Edite o arquivo `.env` com suas configurações:

```env
WHATSAPP_TOKEN=seu_token_aqui
VERIFY_TOKEN=seu_token_de_verificacao
```

### 3. Configuração do Webhook

1. Inicie o servidor localmente:
```bash
python server.py
```

2. Use ngrok ou similar para expor o servidor:
```bash
ngrok http 3000
```

![Configuração Webhook](./images/webhook-setup.png)

## 🎮 Uso

### Iniciando o Servidor

```bash
python server.py
```

O servidor estará disponível em `http://localhost:3000`

### Testando com Postman

1. Importe a coleção do Postman (disponível em `docs/postman`)
2. Configure as variáveis de ambiente no Postman
3. Execute os endpoints de teste

![Teste no Postman](./images/postman-test.png)

## 🤖 Comandos Disponíveis

| Comando | Descrição | Exemplo de Resposta |
|---------|-----------|-------------------|
| hora    | Mostra a hora atual | "Agora são: 14:30:45" |
| data    | Mostra a data atual | "Hoje é: 25/03/2024" |
| ajuda   | Lista todos os comandos | Lista de comandos disponíveis |

## 📁 Estrutura do Projeto

```
whatsapp-webhook/
├── server.py           # Servidor principal
├── requirements.txt    # Dependências
├── .env               # Configurações
├── README.md          # Documentação
├── docs/              # Documentação adicional
├── tests/             # Testes
└── images/            # Imagens da documentação
```

## 🧪 Testes

Execute os testes com:
```bash
pytest tests/
```

## 🤝 Contribuição

1. Fork o projeto
2. Crie sua branch de feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 📸 Capturas de Tela

### Dashboard Principal
![Dashboard](./images/dashboard.png)

### Logs de Mensagens
![Logs](./images/message-logs.png)

### Painel de Administração
![Admin Panel](./images/admin-panel.png)

---

Desenvolvido com ❤️ por Marcelo Henrique

[⬆ Voltar ao topo](#whatsapp-webhook-server) 
