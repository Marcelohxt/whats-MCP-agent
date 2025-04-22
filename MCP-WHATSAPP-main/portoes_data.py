# Dados dos portões disponíveis
PORTÕES = {
    "portao_ferro": {
        "nome": "Portão de Ferro",
        "descricao": "Portão de ferro forjado com design moderno e resistente",
        "imagens": [
            "portoes/ferro/portao1.jpg",
            "portoes/ferro/portao2.jpg",
            "portoes/ferro/portao3.jpg"
        ],
        "preco_base": 2500.00,
        "caracteristicas": [
            "Resistente à corrosão",
            "Design personalizável",
            "Sistema de segurança integrado"
        ]
    },
    "portao_aluminio": {
        "nome": "Portão de Alumínio",
        "descricao": "Portão de alumínio leve e durável",
        "imagens": [
            "portoes/aluminio/portao1.jpg",
            "portoes/aluminio/portao2.jpg",
            "portoes/aluminio/portao3.jpg"
        ],
        "preco_base": 1800.00,
        "caracteristicas": [
            "Leve e durável",
            "Baixa manutenção",
            "Resistente à corrosão"
        ]
    },
    "portao_aco": {
        "nome": "Portão de Aço",
        "descricao": "Portão de aço com alta resistência e segurança",
        "imagens": [
            "portoes/aco/portao1.jpg",
            "portoes/aco/portao2.jpg",
            "portoes/aco/portao3.jpg"
        ],
        "preco_base": 3000.00,
        "caracteristicas": [
            "Alta resistência",
            "Sistema de segurança avançado",
            "Design robusto"
        ]
    }
}

def get_portao_info(tipo: str) -> dict:
    """Retorna informações sobre um tipo específico de portão"""
    return PORTÕES.get(tipo, {})

def get_imagens_portao(tipo: str) -> list:
    """Retorna as imagens disponíveis para um tipo de portão"""
    portao = get_portao_info(tipo)
    return portao.get("imagens", [])

def calcular_orcamento(tipo: str, medidas: dict) -> float:
    """Calcula o orçamento baseado no tipo de portão e medidas"""
    portao = get_portao_info(tipo)
    preco_base = portao.get("preco_base", 0)
    
    # Cálculo simplificado do orçamento
    area = medidas.get("largura", 0) * medidas.get("altura", 0)
    return preco_base * (area / 10)  # Preço por metro quadrado 