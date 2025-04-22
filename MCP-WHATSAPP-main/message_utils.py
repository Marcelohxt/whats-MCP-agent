import re
from typing import Dict, Optional, Tuple
from portoes_data import PORTÕES

def extrair_medidas(mensagem: str) -> Optional[Dict]:
    """Extrai medidas da mensagem no formato 'largura x altura'"""
    padrao = r'(\d+(?:[.,]\d+)?)\s*[xX]\s*(\d+(?:[.,]\d+)?)'
    match = re.search(padrao, mensagem)
    
    if match:
        largura = float(match.group(1).replace(',', '.'))
        altura = float(match.group(2).replace(',', '.'))
        return {"largura": largura, "altura": altura}
    
    return None

def identificar_tipo_portao(mensagem: str) -> str:
    """Identifica o tipo de portão mencionado na mensagem"""
    mensagem = mensagem.lower()
    
    # Mapeamento de palavras-chave para tipos de portão
    palavras_chave = {
        "portao_ferro": ["ferro", "forjado", "ferro forjado"],
        "portao_aluminio": ["aluminio", "alumínio", "alumínio"],
        "portao_aco": ["aço", "aco", "metal", "metálico"]
    }
    
    # Contar ocorrências de cada tipo
    contagem = {tipo: 0 for tipo in PORTÕES.keys()}
    
    for tipo, palavras in palavras_chave.items():
        for palavra in palavras:
            if palavra in mensagem:
                contagem[tipo] += 1
    
    # Retornar o tipo com mais ocorrências
    tipo_mais_comum = max(contagem.items(), key=lambda x: x[1])[0]
    return tipo_mais_comum if contagem[tipo_mais_comum] > 0 else "portao_ferro"  # Default

def extrair_data_horario(mensagem: str) -> Tuple[Optional[str], Optional[str]]:
    """Extrai data e horário da mensagem"""
    # Padrões para data e horário
    padrao_data = r'(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})'
    padrao_horario = r'(\d{1,2})[:h](\d{2})'
    
    # Procurar data
    match_data = re.search(padrao_data, mensagem)
    if match_data:
        dia, mes, ano = match_data.groups()
        data = f"{dia}/{mes}/{ano}"
    else:
        data = None
    
    # Procurar horário
    match_horario = re.search(padrao_horario, mensagem)
    if match_horario:
        hora, minuto = match_horario.groups()
        horario = f"{hora}:{minuto}"
    else:
        horario = None
    
    return data, horario

def formatar_mensagem_orcamento(detalhes: Dict) -> str:
    """Formata os detalhes do orçamento em uma mensagem legível"""
    return f"""*Orçamento para Portão*

Tipo: {detalhes['tipo_portao']}
Medidas: {detalhes['medidas']['largura']}m x {detalhes['medidas']['altura']}m
Valor: R$ {detalhes['valor']:.2f}

Para agendar uma visita técnica, responda com 'AGENDAR'."""

def formatar_mensagem_visita(data: str, horario: str) -> str:
    """Formata os detalhes da visita em uma mensagem legível"""
    return f"""*Visita Técnica Agendada*

Data: {data}
Horário: {horario}

Um de nossos vendedores entrará em contato para confirmar a visita.""" 