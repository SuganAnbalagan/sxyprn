from dataclasses import dataclass
from typing import Optional
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
        video_elements = soup.find_all('div', class_='video-container') or soup.find_all('div', class_='item')
        
        videos = []
        for element in video_elements:
            # Extract video ID from URL pattern
            a_tag = element.find('a')
            if not a_tag:
                continue
                
            url = a_tag.get('href', '')
            video_id = re.search(r'/videos/(\d+)', url)
            if not video_id:
                continue
                
            title = element.find('span', class_='video-title').get_text(strip=True) if element.find('span', class_='video-title') else 'Untitled'
            thumbnail = a_tag.find('img').get('src', '') if a_tag.find('img') else ''
            
            duration = element.find('span', class_='duration').get_text(strip=True) if element.find('span', class_='duration') else None
            
            videos.append(cls(
                id=video_id.group(1),
                title=title,
                thumbnail=thumbnail,
                url=f"{base_url}{url}",
                duration=duration
            ))
            
        return videos