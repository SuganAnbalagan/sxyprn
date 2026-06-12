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
        
        # Comprehensive element search pattern matching across various rendering templates
        video_elements = (
            soup.find_all('div', class_=re.compile(r'd-item|post|item|video-block')) or 
            soup.find_all('a', href=re.compile(r'/\d+/'))
        )
        
        videos = []
        for element in video_elements:
            # Handle if the element container itself is the anchor tag or contains it
            if element.name == 'a':
                a_tag = element
            else:
                a_tag = element.find('a', href=re.compile(r'/\d+/')) or element.find('a')
                
            if not a_tag:
                continue
                
            url = a_tag.get('href', '')
            video_id_match = re.search(r'/(\d+)/|/videos/(\d+)', url)
            if not video_id_match:
                continue
            
            video_id = video_id_match.group(1) or video_id_match.group(2)
                
            # Text parsing fallback loop
            title = 'Untitled'
            title_el = (
                element.find(class_=re.compile(r'title|name|desc')) if element.name != 'a' else None
            ) or a_tag.find('img') or element
            
            if title_el:
                title = title_el.get('alt', '') or title_el.get('title', '') if title_el.name == 'img' else title_el.get_text(strip=True)
            
            if not title or title == 'Untitled':
                title = a_tag.get('title', '') or 'Untitled Video'
                
            # Image extraction fallback loop
            img_tag = element.find('img') if element.name != 'a' else element.find('img')
            thumbnail = ''
            if img_tag:
                thumbnail = img_tag.get('data-src') or img_tag.get('data-original') or img_tag.get('src', '')
            
            # Duration parsing fallback loop
            duration_el = element.find(class_=re.compile(r'duration|time|length')) if element.name != 'a' else None
            duration = duration_el.get_text(strip=True) if duration_el else None
            
            if video_id not in [v.id for v in videos]:
                videos.append(cls(
                    id=video_id,
                    title=title,
                    thumbnail=thumbnail,
                    url=url if url.startswith('http') else f"{base_url.rstrip('/')}{url}",
                    duration=duration
                ))
            
        return videos
