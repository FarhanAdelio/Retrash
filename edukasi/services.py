"""
Service untuk mengambil konten edukasi dari sumber eksternal
"""
import feedparser
import requests
from django.core.cache import cache
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class ExternalContentService:
    """Service untuk fetch konten dari API eksternal"""
    
    # RSS Feed dari berbagai sumber berita lingkungan
    RSS_FEEDS = {
        'greeners': 'https://www.greeners.co/feed/',
        'cnn-teknologi': 'https://www.cnnindonesia.com/teknologi/rss',
    }
    
    # API News (alternatif - butuh API key)
    NEWS_API_KEY = None  # Set di settings.py atau .env
    NEWS_API_URL = 'https://newsapi.org/v2/everything'
    
    @staticmethod
    def get_rss_articles(source='mongabay', limit=10, cache_time=3600):
        """
        Ambil artikel dari RSS Feed
        
        Args:
            source: Nama sumber ('mongabay', 'greeners', dll)
            limit: Jumlah artikel yang diambil
            cache_time: Waktu cache dalam detik (default 1 jam)
        
        Returns:
            List of dict berisi artikel
        """
        cache_key = f'rss_articles_{source}_{limit}'
        
        # Cek cache dulu
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data
        
        try:
            feed_url = ExternalContentService.RSS_FEEDS.get(source)
            if not feed_url:
                logger.error(f"RSS feed source '{source}' tidak ditemukan")
                return []
            
            # Use requests dengan User-Agent untuk bypass blocking
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(feed_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # Parse RSS feed from response content
            feed = feedparser.parse(response.content)
            
            articles = []
            for entry in feed.entries[:limit]:
                article = {
                    'title': entry.get('title', ''),
                    'link': entry.get('link', ''),
                    'description': entry.get('summary', '') or entry.get('description', ''),
                    'published': entry.get('published', ''),
                    'source': source,
                    'image': ExternalContentService._extract_image(entry),
                }
                articles.append(article)
            
            # Simpan ke cache
            cache.set(cache_key, articles, cache_time)
            
            return articles
            
        except Exception as e:
            logger.error(f"Error fetching RSS from {source}: {str(e)}")
            return []
    
    @staticmethod
    def _extract_image(entry):
        """Extract image URL from RSS entry"""
        # Coba dari media content
        if hasattr(entry, 'media_content') and entry.media_content:
            return entry.media_content[0].get('url', '')
        
        # Coba dari media thumbnail
        if hasattr(entry, 'media_thumbnail') and entry.media_thumbnail:
            return entry.media_thumbnail[0].get('url', '')
        
        # Coba dari enclosures
        if hasattr(entry, 'enclosures') and entry.enclosures:
            for enclosure in entry.enclosures:
                if 'image' in enclosure.get('type', ''):
                    return enclosure.get('href', '')
        
        return None
    
    @staticmethod
    def get_all_sources(limit_per_source=5):
        """
        Ambil artikel dari semua sumber RSS
        
        Args:
            limit_per_source: Jumlah artikel per sumber
        
        Returns:
            List of dict berisi semua artikel
        """
        all_articles = []
        
        for source in ExternalContentService.RSS_FEEDS.keys():
            articles = ExternalContentService.get_rss_articles(
                source=source, 
                limit=limit_per_source
            )
            all_articles.extend(articles)
        
        # Sort by published date (newest first)
        all_articles.sort(
            key=lambda x: x.get('published', ''), 
            reverse=True
        )
        
        return all_articles
    
    @staticmethod
    def search_news_api(query='lingkungan sampah', limit=10):
        """
        Search artikel menggunakan News API (butuh API key)
        
        Args:
            query: Kata kunci pencarian
            limit: Jumlah hasil
        
        Returns:
            List of dict berisi artikel
        """
        if not ExternalContentService.NEWS_API_KEY:
            logger.warning("NEWS_API_KEY belum di-set")
            return []
        
        cache_key = f'news_api_{query}_{limit}'
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data
        
        try:
            params = {
                'q': query,
                'language': 'id',
                'sortBy': 'publishedAt',
                'pageSize': limit,
                'apiKey': ExternalContentService.NEWS_API_KEY
            }
            
            response = requests.get(
                ExternalContentService.NEWS_API_URL, 
                params=params,
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            articles = []
            
            for item in data.get('articles', []):
                article = {
                    'title': item.get('title', ''),
                    'link': item.get('url', ''),
                    'description': item.get('description', ''),
                    'published': item.get('publishedAt', ''),
                    'source': item.get('source', {}).get('name', 'News API'),
                    'image': item.get('urlToImage', ''),
                }
                articles.append(article)
            
            # Cache selama 2 jam
            cache.set(cache_key, articles, 7200)
            
            return articles
            
        except Exception as e:
            logger.error(f"Error fetching from News API: {str(e)}")
            return []


class WebScraperService:
    """
    Service untuk web scraping (gunakan dengan hati-hati)
    PENTING: Pastikan comply dengan robots.txt dan terms of service
    """
    
    @staticmethod
    def scrape_article(url):
        """
        Scrape konten artikel dari URL
        
        Args:
            url: URL artikel yang akan di-scrape
        
        Returns:
            Dict berisi konten artikel
        """
        try:
            from bs4 import BeautifulSoup
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (compatible; ReTrashBot/1.0; +https://retrash.id)'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract content (sesuaikan dengan struktur website target)
            title = soup.find('h1')
            title_text = title.get_text(strip=True) if title else ''
            
            # Ambil paragraf
            paragraphs = soup.find_all('p')
            content = '\n\n'.join([p.get_text(strip=True) for p in paragraphs[:10]])
            
            return {
                'title': title_text,
                'content': content,
                'url': url,
                'scraped_at': datetime.now()
            }
            
        except ImportError:
            logger.error("BeautifulSoup4 belum terinstall. Jalankan: pip install beautifulsoup4")
            return None
        except Exception as e:
            logger.error(f"Error scraping {url}: {str(e)}")
            return None
