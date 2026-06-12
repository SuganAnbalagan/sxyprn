from playwright.sync_api import sync_playwright
from typing import List
from models import Video
from config import Config

class Scraper:
    def __init__(self):
        pass
    
    def get_page_html(self, url: str) -> str:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent=Config.HEADERS["User-Agent"],
                viewport={"width": 375, "height": 812},
                is_mobile=True,
                extra_http_headers={"Accept-Encoding": "gzip, deflate"}
            )
            page = context.new_page()
            
            # Block heavy tracking assets and analytics to speed up structural rendering
            page.route("**/*.{png,jpg,jpeg,gif,webp,svg,mp4,woff,woff2,ttf}", lambda route: route.abort())
            
            try:
                page.goto(url, timeout=15000, wait_until="commit")
                page.wait_for_selector('div', timeout=5000)
                html = page.content()
                browser.close()
                return html
            except Exception as e:
                try:
                    html = page.content()
                    browser.close()
                    if len(html) > 500:
                        return html
                except:
                    pass
                browser.close()
                raise Exception(f"Playwright failed to fetch page: {str(e)}")
    
    def scrape_videos(self, url: str) -> List[Video]:
        html = self.get_page_html(url)
        return Video.from_html(html, Config.BASE_URL)
    
    async def async_scrape_videos(self, url: str) -> List[Video]:
        return self.scrape_videos(url)
