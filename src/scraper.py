from playwright.sync_api import sync_playwright
from typing import List
from models import Video
from config import Config

class Scraper:
    def __init__(self):
        # Keeps compatibility with your main.py initialization structure
        pass
    
    def get_page_html(self, url: str) -> str:
        with sync_playwright() as p:
            # Launch a headless browser simulating a mobile profile matching your config
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent=Config.HEADERS["User-Agent"],
                viewport={"width": 375, "height": 812},
                is_mobile=True
            )
            page = context.new_page()
            
            try:
                page.goto(url, timeout=30000, wait_until="networkidle")
                # Extra wait to ensure asynchronous scripts load completely
                page.wait_for_timeout(3000) 
                html = page.content()
                browser.close()
                return html
            except Exception as e:
                browser.close()
                raise Exception(f"Playwright failed to fetch page: {str(e)}")
    
    def scrape_videos(self, url: str) -> List[Video]:
        html = self.get_page_html(url)
        return Video.from_html(html, Config.BASE_URL)
    
    async def async_scrape_videos(self, url: str) -> List[Video]:
        # Fallback to sync wrapper if your app handles routing synchronously
        return self.scrape_videos(url)
