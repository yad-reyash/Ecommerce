import requests
from bs4 import BeautifulSoup
import re
import json

class WebScraper:
    """
    Web scraper for extracting product data from various ecommerce sites.
    Supports Daraz, Nike, Adidas, Amazon, and generic sites.
    """
    
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
    }

    def fetch(self, url):
        """Fetch and parse product data from a given URL."""
        response = requests.get(url, headers=self.HEADERS, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Detect site and use appropriate parser
        if 'daraz' in url.lower():
            return self._parse_daraz(soup, url, response.text)
        elif 'nike.com' in url:
            return self._parse_nike(soup, url)
        elif 'adidas.com' in url:
            return self._parse_adidas(soup, url)
        elif 'amazon' in url:
            return self._parse_amazon(soup, url)
        else:
            return self._parse_generic(soup, url)

    def _parse_daraz(self, soup, url, html_text):
        """Parse Daraz product pages (supports daraz.pk, daraz.com.np, daraz.com.bd, etc.)."""
        products = []
        
        # Method 1: Try to extract from embedded JSON data
        try:
            # Daraz often embeds product data in script tags
            script_tags = soup.find_all('script')
            for script in script_tags:
                if script.string and 'window.pageData' in script.string:
                    # Extract JSON from script
                    json_match = re.search(r'window\.pageData\s*=\s*({.*?});', script.string, re.DOTALL)
                    if json_match:
                        page_data = json.loads(json_match.group(1))
                        items = page_data.get('mods', {}).get('listItems', [])
                        for item in items:
                            product = {
                                'id': item.get('itemId') or item.get('nid'),
                                'name': item.get('name'),
                                'price': item.get('price'),
                                'original_price': item.get('originalPrice'),
                                'discount': item.get('discount'),
                                'image': item.get('image'),
                                'link': f"https://www.daraz.pk/products/{item.get('itemUrl', '')}" if 'daraz.pk' in url else item.get('productUrl'),
                                'rating': item.get('ratingScore'),
                                'reviews': item.get('review'),
                                'location': item.get('location'),
                                'brand': item.get('brandName', 'Daraz'),
                                'source': 'daraz',
                            }
                            if product['name']:
                                products.append(product)
                        if products:
                            return {'products': products, 'source': 'daraz', 'url': url, 'count': len(products)}
        except Exception as e:
            print(f"JSON extraction failed: {e}")
        
        # Method 2: Parse HTML directly
        product_cards = soup.select('[data-qa-locator="product-item"], .gridItem, [class*="product-card"], .c2prKC')
        
        for item in product_cards:
            try:
                product = {
                    'name': self._get_text(item, '[class*="title"], .c16H9d, h2, .RfADt a'),
                    'price': self._get_text(item, '[class*="price"], .c13VH6, .ooOxS'),
                    'original_price': self._get_text(item, '[class*="original"], .c13VH6 del, .WNoq3'),
                    'discount': self._get_text(item, '[class*="discount"], .IcOsH'),
                    'image': self._get_attr(item, 'img', 'src') or self._get_attr(item, 'img', 'data-src'),
                    'link': self._get_attr(item, 'a', 'href'),
                    'rating': self._get_text(item, '[class*="rating"], .c13VH6'),
                    'brand': 'Daraz',
                    'source': 'daraz',
                }
                if product['name']:
                    products.append(product)
            except Exception as e:
                continue
        
        return {'products': products, 'source': 'daraz', 'url': url, 'count': len(products)}

    def _parse_nike(self, soup, url):
        """Parse Nike product pages."""
        products = []
        for item in soup.select('.product-card, .product-grid__item, [data-testid="product-card"]'):
            product = {
                'name': self._get_text(item, '.product-card__title, h2, h3'),
                'price': self._get_text(item, '.product-card__price, .product-price'),
                'image': self._get_attr(item, 'img', 'src'),
                'link': self._get_attr(item, 'a', 'href'),
                'brand': 'Nike',
            }
            if product['name']:
                products.append(product)
        return {'products': products, 'source': 'nike', 'url': url}

    def _parse_adidas(self, soup, url):
        """Parse Adidas product pages."""
        products = []
        for item in soup.select('.product-card, .glass-product-card, [data-auto-id="product-card"]'):
            product = {
                'name': self._get_text(item, '.product-card__title, .glass-product-card__title'),
                'price': self._get_text(item, '.product-card__price, .gl-price'),
                'image': self._get_attr(item, 'img', 'src'),
                'link': self._get_attr(item, 'a', 'href'),
                'brand': 'Adidas',
            }
            if product['name']:
                products.append(product)
        return {'products': products, 'source': 'adidas', 'url': url}

    def _parse_amazon(self, soup, url):
        """Parse Amazon product pages."""
        products = []
        for item in soup.select('.s-result-item[data-component-type="s-search-result"]'):
            product = {
                'name': self._get_text(item, 'h2 span, .a-text-normal'),
                'price': self._get_text(item, '.a-price .a-offscreen, .a-price-whole'),
                'image': self._get_attr(item, '.s-image', 'src'),
                'link': self._get_attr(item, 'a.a-link-normal', 'href'),
                'rating': self._get_text(item, '.a-icon-alt'),
                'brand': 'Various',
            }
            if product['name']:
                products.append(product)
        return {'products': products, 'source': 'amazon', 'url': url}

    def _parse_generic(self, soup, url):
        """Generic parser for unknown sites."""
        products = []
        
        # Try common product card selectors
        selectors = [
            '.product', '.product-card', '.product-item', 
            '[class*="product"]', '.item', '.card'
        ]
        
        for selector in selectors:
            items = soup.select(selector)
            if items:
                for item in items[:20]:  # Limit to 20 products
                    product = {
                        'name': self._get_text(item, 'h2, h3, h4, .title, .name, [class*="title"], [class*="name"]'),
                        'price': self._get_text(item, '.price, [class*="price"], .cost'),
                        'image': self._get_attr(item, 'img', 'src'),
                        'link': self._get_attr(item, 'a', 'href'),
                    }
                    if product['name'] and product['name'] not in [p['name'] for p in products]:
                        products.append(product)
                break
        
        return {'products': products, 'source': 'generic', 'url': url}

    def _get_text(self, element, selector):
        """Safely extract text from an element."""
        try:
            el = element.select_one(selector)
            return el.get_text(strip=True) if el else None
        except:
            return None

    def _get_attr(self, element, selector, attr):
        """Safely extract attribute from an element."""
        try:
            el = element.select_one(selector)
            return el.get(attr) if el else None
        except:
            return None

    def search_shoes(self, query, site='all'):
        """Search for shoes across multiple sites including Daraz."""
        results = []
        
        search_urls = {
            'daraz': f'https://www.daraz.pk/catalog/?q={query}',
            'daraz_np': f'https://www.daraz.com.np/catalog/?q={query}',
            'daraz_bd': f'https://www.daraz.com.bd/catalog/?q={query}',
            'nike': f'https://www.nike.com/w?q={query}&vst={query}',
            'adidas': f'https://www.adidas.com/us/search?q={query}',
            'amazon': f'https://www.amazon.com/s?k={query}+shoes',
        }
        
        sites_to_search = [site] if site != 'all' else search_urls.keys()
        
        for site_name in sites_to_search:
            if site_name in search_urls:
                try:
                    data = self.fetch(search_urls[site_name])
                    results.extend(data.get('products', []))
                except Exception as e:
                    print(f"Error scraping {site_name}: {e}")
        
        return {'products': results, 'query': query}
