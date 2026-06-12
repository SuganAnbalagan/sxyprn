import requests
from bs4 import BeautifulSoup
import asyncio
import aiohttp
from typing import List
from models import Video
from config import Config

class Scraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(Config.HEADERS)
    
    def get_page_html(self, url: str) -> str:
        for attempt in range(Config.MAX_RETRIES):
            try:
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                return response.text
            except Exception as e:
                if attempt == Config.MAX_RETRIES - 1:
                    raise Exception(f"Failed to fetch page after {Config.MAX_RETRIES} attempts: {str(e)}")
                continue
    
    def scrape_videos(self, url: str) -> List[Video]:
        html = self.get_page_html(url)
        return Video.from_html(html, Config.BASE_URL)
    
    async def async_scrape_videos(self, url: str) -> List[Video]:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=Config.HEADERS, timeout=10) as response:
                if response.status == 200:
                    html = await response.text()
                    return Video.from_html(html, Config.BASE_URL)
                else:
                    raise Exception(f"Failed to fetch page: {response.status}")