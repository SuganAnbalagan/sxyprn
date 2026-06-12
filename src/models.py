from dataclasses import dataclass
from typing import Optional
from bs4 import BeautifulSoup
import re

@dataclass
class Video:
    id: str
    title: str
    thumbnail: str
    url: str
    duration: Optional[str] = None
    views: Optional[str] = None
    date: Optional[str] = None

    @classmethod
    def from_html(cls, html: str, base_url: str):
        soup = BeautifulSoup(html, 'html.parser')
        
        # Target the post elements used by the site structure
        video_elements = soup.find_all('div', class_=re.compile(r'post|item|video'))
        
        videos = []
        for element in video_elements:
            a_tag = element.find('a', href=re.compile(r'/\d+/')) or element.find('a')
            if not a_tag:
                continue
                
            url = a_tag.get('href', '')
            # Match either /videos/id or the site's /id/title format
            video_id_match = re.search(r'/(\d+)/|/videos/(\d+)', url)
            if not video_id_match:
                continue
            
            # Extract whichever group matched the numerical ID
            video_id = video_id_match.group(1) or video_id_match.group(2)
                
            # Fallback chain for titles
            title_el = element.find('span', class_='title') or element.find('div', class_='title') or element.find('img')
            title = 'Untitled'
            if title_el:
                title = title_el.get('alt', '') if title_el.name == 'img' else title_el.get_text(strip=True)
                
            # Thumbnail extraction
            img_tag = element.find('img')
            thumbnail = ''
            if img_tag:
                thumbnail = img_tag.get('data-src') or img_tag.get('src', '')
            
            # Duration extraction 
            duration_el = element.find('span', class_='duration') or element.find('div', class_='time')
            duration = duration_el.get_text(strip=True) if duration_el else None
            
            # Avoid duplicating video entries
            if video_id not in [v.id for v in videos]:
                videos.append(cls(
                    id=video_id,
                    title=title,
                    thumbnail=thumbnail,
                    url=url if url.startswith('http') else f"{base_url.rstrip('/')}{url}",
                    duration=duration
                ))
            
        return videos
