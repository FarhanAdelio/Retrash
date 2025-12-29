#!/usr/bin/env python
"""
Script untuk testing RSS feed dari Detik.com
"""
import feedparser

# Test semua URL RSS Detik
feeds = {
    'detik-bank-sampah': 'https://www.detik.com/tag/bank-sampah/rss',
    'detik-lingkungan': 'https://www.detik.com/tag/lingkungan/rss',
    'detik-daur-ulang': 'https://www.detik.com/tag/daur-ulang/rss',
    'detik-sampah': 'https://www.detik.com/tag/sampah/rss',
}

print("=" * 80)
print("TESTING RSS FEEDS FROM DETIK.COM")
print("=" * 80)

for name, url in feeds.items():
    print(f"\n{'=' * 80}")
    print(f"Testing: {name}")
    print(f"URL: {url}")
    print("-" * 80)
    
    try:
        feed = feedparser.parse(url)
        
        print(f"Status: {feed.get('status', 'Unknown')}")
        print(f"Total entries: {len(feed.entries)}")
        
        if feed.entries:
            print(f"\n✅ SUCCESS! Ditemukan {len(feed.entries)} artikel")
            print("\nContoh 3 artikel pertama:")
            for i, entry in enumerate(feed.entries[:3], 1):
                print(f"\n{i}. {entry.get('title', 'No title')}")
                print(f"   Link: {entry.get('link', 'No link')}")
                print(f"   Published: {entry.get('published', 'No date')}")
        else:
            print("❌ TIDAK ADA ARTIKEL DITEMUKAN")
            print(f"Feed info: {feed.get('feed', {})}")
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")

print("\n" + "=" * 80)
print("TESTING SELESAI")
print("=" * 80)
