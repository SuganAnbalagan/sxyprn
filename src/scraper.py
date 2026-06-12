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
                viewport={"width": 1280, "height": 1000}, # Use desktop viewport size to force more content blocks into view
                is_mobile=False,
                extra_http_headers={"Accept-Encoding": "gzip, deflate"}
            )
            page = context.new_page()
            
            # Allow basic layout assets but block external tracker domains
            page.route("**/*.{mp4,ogv,webm,woff,woff2}", lambda route: route.abort())
            
            try:
                page.goto(url, timeout=20000, wait_until="domcontentloaded")
                
                # Force dynamic lazyload execution by scrolling down the screen layout structure
                for _ in range(3):
                    page.evaluate("window.scrollBy(0, 800)")
                    page.wait_for_timeout(500)
                
                # Explicit fallback wait condition to guarantee script evaluations complete
                page.wait_for_timeout(2000)
                
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
