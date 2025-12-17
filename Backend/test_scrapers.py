"""Test Jeevee and Daraz scrapers"""
from scraper.jeevee import JeeveeScraper
from scraper.daraz import DarazScraper

def test_jeevee():
    print("=== Jeevee Test ===")
    s = JeeveeScraper()
    r = s.search('phone', limit=5)
    
    print(f"Found: {len(r['products'])} products")
    print()
    
    for i, p in enumerate(r['products'][:5], 1):
        name = p.get('name', 'N/A')[:40]
        price = p.get('price', 'N/A')
        url = p.get('url', 'N/A')[:60]
        print(f"{i}. {name}")
        print(f"   Price: Rs. {price}")
        print(f"   URL: {url}...")
        print()

def test_daraz():
    print("=== Daraz Test ===")
    s = DarazScraper(region='np')
    r = s.search('phone')
    
    print(f"Found: {len(r['products'])} products")
    print()
    
    for i, p in enumerate(r['products'][:5], 1):
        name = p.get('name', 'N/A')[:40]
        price = p.get('price', 'N/A')
        url = p.get('url', 'N/A')[:60] if p.get('url') else 'N/A'
        print(f"{i}. {name}")
        print(f"   Price: Rs. {price}")
        print(f"   URL: {url}")
        print()

if __name__ == '__main__':
    test_jeevee()
    print("\n" + "="*50 + "\n")
    test_daraz()
