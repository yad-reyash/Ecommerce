"""
Daraz Scraper Module
Supports daraz.pk, daraz.com.np, daraz.com.bd, daraz.lk
Uses undetected-chromedriver for bypassing anti-bot protection.
"""
import requests
from bs4 import BeautifulSoup
import json
import re
import time
from urllib.parse import quote, urljoin

# Undetected Chrome imports (best for anti-bot bypass)
try:
    import undetected_chromedriver as uc
    UNDETECTED_AVAILABLE = True
except ImportError:
    UNDETECTED_AVAILABLE = False

# Regular Selenium imports as fallback
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from webdriver_manager.chrome import ChromeDriverManager
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False


class DarazScraper:
    """
    Specialized scraper for Daraz ecommerce platform.
    Uses Selenium to bypass anti-bot protection.
    """
    
    BASE_URLS = {
        'pk': 'https://www.daraz.pk',
        'np': 'https://www.daraz.com.np',
        'bd': 'https://www.daraz.com.bd',
        'lk': 'https://www.daraz.lk',
    }
    
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
    }
    
    def __init__(self, region='np'):
        """Initialize with a specific region (default: Nepal)."""
        self.region = region
        self.base_url = self.BASE_URLS.get(region, self.BASE_URLS['np'])
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)
        self.driver = None
    
    def _init_driver(self):
        """Initialize WebDriver with undetected-chromedriver for anti-bot bypass."""
        if self.driver is not None:
            return self.driver
        
        # Try undetected-chromedriver first (best for anti-bot)
        if UNDETECTED_AVAILABLE:
            try:
                options = uc.ChromeOptions()
                # Note: headless mode often gets detected by anti-bot
                # Using headless=new with extra stealth settings
                options.add_argument('--headless=new')
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument('--disable-gpu')
                options.add_argument('--window-size=1920,1080')
                options.add_argument('--disable-extensions')
                options.add_argument('--disable-infobars')
                options.add_argument('--disable-blink-features=AutomationControlled')
                options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
                
                self.driver = uc.Chrome(options=options, use_subprocess=True)
                # Set page load timeout
                self.driver.set_page_load_timeout(45)
                self.driver.implicitly_wait(10)
                print("[Daraz] Using undetected-chromedriver")
                return self.driver
            except Exception as e:
                print(f"[Daraz] Undetected Chrome failed: {e}, trying regular Selenium")
                # Continue to regular Selenium instead of trying non-headless
        
        # Fallback to regular Selenium
        if SELENIUM_AVAILABLE:
            options = Options()
            options.add_argument('--headless=new')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--window-size=1920,1080')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
            options.add_experimental_option('excludeSwitches', ['enable-automation'])
            options.add_experimental_option('useAutomationExtension', False)
            options.add_argument('--log-level=3')
            
            try:
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=options)
                self.driver.set_page_load_timeout(30)
                self.driver.implicitly_wait(10)
                
                self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                    'source': '''
                        Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
                    '''
                })
                print("[Daraz] Using regular Selenium")
                return self.driver
            except Exception as e:
                print(f"[Daraz] Regular Selenium failed: {e}")
        
        raise ImportError("No WebDriver available. Install: pip install undetected-chromedriver")
    
    def _close_driver(self):
        """Close the WebDriver safely."""
        if self.driver:
            try:
                self.driver.quit()
            except Exception as e:
                print(f"[Daraz] Error closing driver: {e}")
            finally:
                self.driver = None
    
    def __del__(self):
        """Cleanup driver on object destruction."""
        self._close_driver()
    
    def search(self, query, page=1, limit=40, sort='popularity'):
        """
        Search for products on Daraz using Selenium.
        
        Args:
            query: Search term
            page: Page number (1-indexed)
            limit: Maximum number of products to return
            sort: Sort order - 'popularity', 'price_low', 'price_high', 'newest'
        
        Returns:
            dict with products list and metadata
        """
        sort_map = {
            'popularity': 'popularity',
            'price_low': 'priceasc',
            'price_high': 'pricedesc',
            'newest': 'recent',
        }
        
        # Try Selenium method first (bypasses anti-bot)
        products = self._fetch_via_selenium(query, page, sort_map.get(sort, 'popularity'))
        
        if products:
            return {
                'success': True,
                'products': products[:limit],
                'count': len(products[:limit]),
                'total': len(products),
                'query': query,
                'page': page,
                'source': 'daraz',
                'region': self.region,
            }
        
        # Fallback to requests (may be blocked)
        result = self._fetch_via_requests(query, page, sort_map.get(sort, 'popularity'), limit)
        
        # If anti-bot detected, return empty but graceful response
        if result.get('error') == 'Anti-bot protection detected':
            print("[Daraz] Anti-bot protection active - Daraz temporarily unavailable")
            return {
                'success': False,
                'products': [],
                'count': 0,
                'query': query,
                'page': page,
                'source': 'daraz',
                'region': self.region,
                'error': 'Daraz temporarily unavailable due to anti-bot protection. Try again later.',
            }
        
        return result
    
    def _fetch_via_selenium(self, query, page=1, sort='popularity'):
        """Fetch products using Selenium to bypass anti-bot."""
        products = []
        
        try:
            driver = self._init_driver()
            
            url = f"{self.base_url}/catalog/?q={quote(query)}&page={page}&sort={sort}"
            print(f"[Daraz] Fetching: {url}")
            
            try:
                driver.get(url)
            except Exception as e:
                print(f"[Daraz] Page load timeout/error: {e}")
                # Try to get whatever content we have
            
            # Wait for page to load (increased time for anti-bot)
            time.sleep(4)
            
            # Wait for products to appear with multiple selectors
            selectors = [
                '[data-qa-locator="product-item"]',
                '.Bm3ON',
                '.gridItem',
                '[class*="product-card"]',
                '.buTCk',  # Daraz Nepal specific
                '.qmXQo',  # Another Daraz selector
            ]
            
            found = False
            for selector in selectors:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        print(f"[Daraz] Found {len(elements)} items with selector: {selector}")
                        found = True
                        break
                except:
                    continue
            
            if not found:
                print("[Daraz] No products found with any selector, checking page source...")
            
            # Scroll to load more products
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
                time.sleep(1)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
            except:
                pass
            
            # Get page source
            html = driver.page_source
            
            # Try to extract from embedded JSON first
            products = self._extract_from_page_data(html)
            
            # If no products from JSON, parse HTML
            if not products:
                soup = BeautifulSoup(html, 'html.parser')
                products = self._parse_html_products(soup)
            
            print(f"[Daraz] Found {len(products)} products")
            
        except Exception as e:
            print(f"[Daraz] Selenium error: {e}")
        
        return products
    
    def _fetch_via_requests(self, query, page=1, sort='popularity', limit=40):
        """Fallback: Fetch products using requests."""
        products = []
        
        try:
            url = f"{self.base_url}/catalog/?q={quote(query)}&page={page}&sort={sort}"
            response = self.session.get(url, timeout=15)
            
            if response.status_code == 200:
                html = response.text
                
                # Check for anti-bot
                if 'x5secdata' in html or 'captcha' in html.lower():
                    print("[Daraz] Anti-bot detected in requests fallback")
                    return {
                        'success': False,
                        'products': [],
                        'count': 0,
                        'error': 'Anti-bot protection detected',
                        'source': 'daraz',
                    }
                
                products = self._extract_from_page_data(html)
                
                if not products:
                    soup = BeautifulSoup(html, 'html.parser')
                    products = self._parse_html_products(soup)
        except Exception as e:
            print(f"[Daraz] Requests error: {e}")
        
        return {
            'success': len(products) > 0,
            'products': products[:limit],
            'count': len(products[:limit]),
            'query': query,
            'page': page,
            'source': 'daraz',
            'region': self.region,
        }
    
    def _extract_from_page_data(self, html):
        """Extract product data from embedded JavaScript."""
        products = []
        
        try:
            patterns = [
                r'window\.pageData\s*=\s*({.*?});?\s*</script>',
                r'"listItems"\s*:\s*(\[.*?\])\s*,\s*"',
                r'window\.__INITIAL_STATE__\s*=\s*({.*?});?\s*</script>',
            ]
            
            for pattern in patterns:
                match = re.search(pattern, html, re.DOTALL)
                if match:
                    try:
                        json_str = match.group(1)
                        data = json.loads(json_str)
                        
                        items = []
                        if isinstance(data, list):
                            items = data
                        elif isinstance(data, dict):
                            items = (
                                data.get('mods', {}).get('listItems', []) or
                                data.get('listItems', []) or
                                data.get('items', []) or
                                []
                            )
                        
                        for item in items:
                            product = self._normalize_product(item)
                            if product.get('name'):
                                products.append(product)
                        
                        if products:
                            break
                    except json.JSONDecodeError:
                        continue
        except Exception as e:
            print(f"[Daraz] JSON extraction error: {e}")
        
        return products
    
    def _parse_html_products(self, soup):
        """Parse products from HTML when JSON is not available."""
        products = []
        
        selectors = [
            '[data-qa-locator="product-item"]',
            'div.Bm3ON',
            'div.gridItem',
            '[data-tracking="product-card"]',
            'div[class*="product-card"]',
        ]
        
        for selector in selectors:
            items = soup.select(selector)
            if items and len(items) >= 1:
                print(f"[Daraz] Found {len(items)} items with selector: {selector}")
                for item in items[:40]:
                    try:
                        product = self._parse_product_card(item)
                        if product.get('name'):
                            products.append(product)
                    except Exception as e:
                        continue
                
                if products:
                    break
        
        return products
    
    def _parse_product_card(self, card):
        """Parse a single product card."""
        # Find link
        link_el = card.select_one('a[href*="/products/"]') or card.select_one('a')
        link = link_el.get('href') if link_el else None
        
        # Find name
        name_el = (
            card.select_one('.RfADt a') or
            card.select_one('[class*="title"]') or
            card.select_one('h2 a') or
            card.select_one('a[title]')
        )
        name = name_el.get_text(strip=True) if name_el else None
        if not name and name_el:
            name = name_el.get('title')
        
        # Find price
        price_el = (
            card.select_one('.ooOxS') or
            card.select_one('[class*="price"]') or
            card.select_one('span[class*="currency"]')
        )
        price_text = price_el.get_text(strip=True) if price_el else None
        price = self._parse_price(price_text)
        
        # Find original price
        orig_price_el = card.select_one('.WNoq3') or card.select_one('del')
        orig_price_text = orig_price_el.get_text(strip=True) if orig_price_el else None
        original_price = self._parse_price(orig_price_text)
        
        # Find discount
        discount_el = card.select_one('.IcOsH') or card.select_one('[class*="discount"]')
        discount = discount_el.get_text(strip=True) if discount_el else None
        
        # Find image
        img_el = card.select_one('img')
        image = None
        if img_el:
            image = img_el.get('src') or img_el.get('data-src')
        
        # Find rating
        rating_el = card.select_one('[class*="rating"]')
        rating = rating_el.get_text(strip=True) if rating_el else None
        
        # Build full URL
        if link and not link.startswith('http'):
            link = urljoin(self.base_url, link)
        
        return {
            'name': name,
            'price': price,
            'original_price': original_price,
            'discount': discount,
            'image': image,
            'url': link,
            'link': link,
            'rating': rating,
            'source': 'Daraz',
            'currency': 'NPR' if self.region == 'np' else 'PKR',
            'in_stock': True,
        }
    
    def _normalize_product(self, item):
        """Normalize product data from JSON formats."""
        price = item.get('price') or item.get('priceShow') or item.get('salePrice')
        if isinstance(price, str):
            price = self._parse_price(price)
        
        original_price = item.get('originalPrice') or item.get('originalPriceShow')
        if isinstance(original_price, str):
            original_price = self._parse_price(original_price)
        
        link = self._build_product_link(item)
        
        return {
            'id': str(item.get('itemId') or item.get('nid') or item.get('id', '')),
            'name': item.get('name') or item.get('title'),
            'price': price,
            'original_price': original_price,
            'discount': item.get('discount') or item.get('discountShow'),
            'image': item.get('image') or item.get('img') or item.get('thumbUrl'),
            'url': link,
            'link': link,
            'rating': item.get('ratingScore') or item.get('rating'),
            'review_count': item.get('review') or item.get('reviewCount') or 0,
            'sold': item.get('itemSoldCntShow') or item.get('sold'),
            'location': item.get('location') or item.get('sellerLocation'),
            'brand': item.get('brandName'),
            'source': 'Daraz',
            'currency': 'NPR' if self.region == 'np' else 'PKR',
            'in_stock': True,
        }
    
    def _build_product_link(self, item):
        """Build product URL from item data."""
        if item.get('productUrl'):
            url = item['productUrl']
        elif item.get('itemUrl'):
            url = item['itemUrl']
        elif item.get('itemId'):
            url = f"/products/i{item['itemId']}.html"
        else:
            return None
        
        if not url.startswith('http'):
            url = urljoin(self.base_url, url)
        return url
    
    def _parse_price(self, price_str):
        """Parse price from string to float."""
        if not price_str:
            return None
        try:
            # Remove currency symbols, "Rs", "NPR", "PKR" and whitespace
            cleaned = str(price_str)
            cleaned = re.sub(r'(Rs\.?|NPR|PKR|रू)', '', cleaned, flags=re.IGNORECASE)
            # Remove commas used as thousand separators
            cleaned = cleaned.replace(',', '')
            # Extract the numeric part
            match = re.search(r'[\d.]+', cleaned)
            if match:
                return float(match.group())
            return None
        except:
            return None
    
    def get_product_details(self, product_url):
        """Get detailed information about a specific product."""
        if not product_url.startswith('http'):
            product_url = f"{self.base_url}/products/{product_url}"
        
        try:
            driver = self._init_driver()
            driver.get(product_url)
            time.sleep(2)
            
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            
            # Try JSON-LD first
            script = soup.find('script', type='application/ld+json')
            if script:
                try:
                    data = json.loads(script.string)
                    return self._parse_product_json_ld(data)
                except:
                    pass
            
            return self._parse_product_html(soup, product_url)
            
        except Exception as e:
            return {'error': str(e), 'url': product_url}
    
    def _parse_product_json_ld(self, data):
        """Parse product details from JSON-LD."""
        if isinstance(data, list):
            data = data[0] if data else {}
        
        return {
            'name': data.get('name'),
            'description': data.get('description'),
            'price': data.get('offers', {}).get('price'),
            'currency': data.get('offers', {}).get('priceCurrency'),
            'image': data.get('image'),
            'brand': data.get('brand', {}).get('name'),
            'rating': data.get('aggregateRating', {}).get('ratingValue'),
            'reviews': data.get('aggregateRating', {}).get('reviewCount'),
            'source': 'Daraz',
        }
    
    def _parse_product_html(self, soup, url):
        """Parse product details from HTML."""
        name_el = soup.select_one('.pdp-mod-product-badge-title, h1')
        price_el = soup.select_one('.pdp-price, [class*="price-current"]')
        
        return {
            'name': name_el.get_text(strip=True) if name_el else None,
            'price': self._parse_price(price_el.get_text(strip=True)) if price_el else None,
            'url': url,
            'source': 'Daraz',
        }
    
    def __del__(self):
        """Cleanup WebDriver on deletion."""
        self._close_driver()


# Convenience function
def search_daraz(query, region='np', page=1, limit=40):
    """Quick search function."""
    scraper = DarazScraper(region=region)
    result = scraper.search(query, page=page, limit=limit)
    scraper._close_driver()
    return result
