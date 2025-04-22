from serralheria_agent import SerralheriaAgent

def test_agent():
    print("Iniciando teste do SerralheriaAgent...")
    agent = SerralheriaAgent()
    
    # Teste de mensagem simples
    mensagem = "Olá, preciso de um orçamento para um portão basculante de 3x2.5 metros"
    print("\nEnviando mensagem:", mensagem)
    
    try:
        resposta = agent.processar_mensagem(mensagem)
        print("\nResposta do agente:")
        print("-" * 50)
        print(resposta)
        print("-" * 50)
        return True
    except Exception as e:
        print("\nErro ao processar mensagem:")
        print(str(e))
        return False

if __name__ == "__main__":
    test_agent() 