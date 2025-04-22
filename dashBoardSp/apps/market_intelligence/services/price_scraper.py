import asyncio
import aiohttp
from bs4 import BeautifulSoup
from typing import List, Dict
import pandas as pd
from datetime import datetime
import re

class PriceScraperService:
    def __init__(self):
        self.sources = {
            'leroy': {
                'name': 'Leroy Merlin',
                'base_url': 'https://www.leroymerlin.com.br/search?term=',
                'region': 'Nacional'
            },
            'telhanorte': {
                'name': 'Telha Norte',
                'base_url': 'https://www.telhanorte.com.br/busca?q=',
                'region': 'Nacional'
            },
            'cec': {
                'name': 'C&C',
                'base_url': 'https://www.cec.com.br/busca?q=',
                'region': 'Nacional'
            },
            'tumelero': {
                'name': 'Tumelero',
                'base_url': 'https://www.tumelero.com.br/busca?q=',
                'region': 'Sul'
            },
            'cassol': {
                'name': 'Cassol',
                'base_url': 'https://www.cassol.com.br/busca?q=',
                'region': 'Sul'
            }
            # Adicionar mais fontes conforme necessário
        }
        
    async def fetch_page(self, session: aiohttp.ClientSession, url: str, headers: Dict) -> str:
        try:
            async with session.get(url, headers=headers) as response:
                return await response.text()
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return ""

    async def search_material(self, material: str) -> List[Dict]:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        async with aiohttp.ClientSession() as session:
            tasks = []
            for source in self.sources.values():
                url = source['base_url'] + material.replace(' ', '+')
                tasks.append(self.fetch_page(session, url, headers))
            
            pages = await asyncio.gather(*tasks)
            results = []
            
            for source, page in zip(self.sources.values(), pages):
                if page:
                    items = await self.parse_page(page, source)
                    results.extend(items)
            
            return sorted(results, key=lambda x: float(x['price']))

    async def parse_page(self, html: str, source: Dict) -> List[Dict]:
        soup = BeautifulSoup(html, 'html.parser')
        results = []
        
        # Adaptar os seletores para cada site
        if source['name'] == 'Leroy Merlin':
            products = soup.find_all('div', class_='product-card')
            for product in products:
                try:
                    name = product.find('h2', class_='product-title').text.strip()
                    price = product.find('span', class_='price').text.strip()
                    url = product.find('a')['href']
                    price = float(re.sub(r'[^\d,]', '', price).replace(',', '.'))
                    
                    results.append({
                        'store_name': source['name'],
                        'product_name': name,
                        'price': price,
                        'url': url,
                        'region': source['region']
                    })
                except:
                    continue
        
        # Adicionar mais parsers para outros sites
        
        return results

    def process_bulk_file(self, file_path: str) -> pd.DataFrame:
        try:
            # Ler arquivo Excel ou CSV
            if file_path.endswith('.xlsx'):
                df = pd.read_excel(file_path)
            else:
                df = pd.read_csv(file_path)
            
            results = []
            for material in df['material']:
                quotes = asyncio.run(self.search_material(material))
                results.extend(quotes)
            
            return pd.DataFrame(results)
        except Exception as e:
            print(f"Error processing file: {e}")
            return pd.DataFrame()

    def generate_report(self, quotes: List[Dict], output_format: str = 'excel') -> str:
        df = pd.DataFrame(quotes)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if output_format == 'excel':
            filename = f'cotacao_{timestamp}.xlsx'
            df.to_excel(f'media/results/{filename}', index=False)
        else:
            filename = f'cotacao_{timestamp}.pdf'
            # Usar reportlab ou weasyprint para gerar PDF
            
        return filename 