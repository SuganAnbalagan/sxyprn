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
        videos = []
        
        # Extract every absolute external video reference node directly
        all_links = soup.find_all('a', href=True)
        
        for link in all_links:
            url = link.get('href', '')
            
            # Find external dynamic distribution stream providers embedded in the string block
            if 'vidara.so/v/' in url or 'lulustream.com/' in url or 'luluvid.com/' in url:
                # Isolate the platform's routing hash to use as a primary key ID
                video_id_match = re.search(r'/v/([A-Za-z0-9]+)|/([A-Za-z0-9]+)$', url)
                if not video_id_match:
                    continue
                video_id = next(g for g in video_id_match.groups() if g is not None)
                
                # Traverse backward through sibling elements to capture the raw title metadata context
                title = "Untitled Video"
                parent = link.parent
                if parent:
                    # Capture the textual information preceding the link target
                    text_content = parent.get_text(" ", strip=True)
                    # Extract string components located ahead of the outbound stream URL
                    if url in text_content:
                        title_part = text_content.split(url)[0].strip()
                        # Clean out residual structural elements
                        title_part = re.sub(r'FULL HD.*$', '', title_part, flags=re.IGNORECASE)
                        title_part = re.sub(r'WATCH FULL.*$', '', title_part, flags=re.IGNORECASE)
                        if title_part:
                            title = title_part[-200:] # Limit string length bounds
                
                # Assign default placeholder image maps when hidden behind lazyloading configurations
                thumbnail = 'https://via.placeholder.com/320x180/1f1f1f/666666?text=Video+Source'
                
                if video_id not in [v.id for v in videos]:
                    videos.append(cls(
                        id=video_id,
                        title=title,
                        thumbnail=thumbnail,
                        url=url,
                        duration="HD"
                    ))
                    
        return videos
