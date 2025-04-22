import requests
from bs4 import BeautifulSoup
from datetime import datetime
from newspaper import Article
import asyncio
import aiohttp
from typing import List, Dict

class ConstructionNewsScraperService:
    def __init__(self):
        self.sources = {
            'sinduscon': 'https://www.sindusconsp.com.br/noticias/',
            'cbic': 'https://cbic.org.br/noticias/',
            'piniweb': 'https://www.piniweb.com.br/noticias/',
        }
        
    async def fetch_page(self, session: aiohttp.ClientSession, url: str) -> str:
        try:
            async with session.get(url) as response:
                return await response.text()
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return ""

    async def parse_article(self, url: str) -> Dict:
        try:
            article = Article(url)
            article.download()
            article.parse()
            article.nlp()
            
            return {
                'title': article.title,
                'text': article.text,
                'summary': article.summary,
                'keywords': article.keywords,
                'published_date': article.publish_date,
                'url': url
            }
        except Exception as e:
            print(f"Error parsing article {url}: {e}")
            return {}

    async def get_construction_news(self) -> List[Dict]:
        async with aiohttp.ClientSession() as session:
            tasks = []
            for source, url in self.sources.items():
                tasks.append(self.fetch_page(session, url))
            
            pages = await asyncio.gather(*tasks)
            news_items = []
            
            for source, page in zip(self.sources.keys(), pages):
                if page:
                    soup = BeautifulSoup(page, 'html.parser')
                    # Adaptar os seletores conforme necessário
                    articles = soup.find_all('article')
                    
                    for article in articles[:5]:  # Limitar a 5 notícias por fonte
                        link = article.find('a')
                        if link and link.get('href'):
                            article_data = await self.parse_article(link['href'])
                            if article_data:
                                article_data['source'] = source
                                news_items.append(article_data)
            
            return news_items

class ConstructionIndexScraperService:
    def __init__(self):
        self.sources = {
            'sinapi': 'https://www.ibge.gov.br/estatisticas/economicas/precos-e-custos/9270-sistema-nacional-de-pesquisa-de-custos-e-indices-da-construcao-civil.html',
            'incc': 'https://www.portalibre.fgv.br/estudos-e-pesquisas/indices-de-precos/incc'
        }

    async def get_construction_indices(self) -> List[Dict]:
        # Implementar scraping dos índices
        pass

class MaterialPriceScraperService:
    def __init__(self):
        self.sources = {
            'material_prices': 'https://www.sienge.com.br/blog/tabela-de-precos-materiais-de-construcao/'
        }

    async def get_material_prices(self) -> List[Dict]:
        # Implementar scraping dos preços
        pass 