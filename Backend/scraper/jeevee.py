"""
Jeevee.com Web Scraper for Nepal Market
Scrapes products from Jeevee's API
"""

import requests
import logging
from typing import Dict, List, Optional
from urllib.parse import quote

logger = logging.getLogger(__name__)


class JeeveeScraper:
    """Scraper for Jeevee.com - Nepal's health and lifestyle e-commerce platform"""
    
    BASE_URL = "https://api.jeevee.com"
    WEBSITE_URL = "https://jeevee.com"
    
    DEFAULT_HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.9',
        'Origin': 'https://jeevee.com',
        'Referer': 'https://jeevee.com/',
    }
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(self.DEFAULT_HEADERS)
    
    def search(self, query: str, page: int = 1, limit: int = 20) -> Dict:
        """
        Search for products on Jeevee
        
        Args:
            query: Search term
            page: Page number (default 1)
            limit: Number of results per page (default 20)
            
        Returns:
            Dictionary with products and metadata
        """
        try:
            encoded_query = quote(query)
            url = f"{self.BASE_URL}/products?search={encoded_query}&page={page}&limit={limit}"
            
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            products = self._parse_products(data.get('data', []))
            
            return {
                'success': True,
                'products': products,
                'total': data.get('total_results', 0),
                'page': data.get('page', page),
                'total_pages': data.get('total_pages', 1),
                'has_next': data.get('has_next', False),
                'has_prev': data.get('has_prev', False),
                'source': 'jeevee',
                'query': query
            }
            
        except requests.RequestException as e:
            logger.error(f"Jeevee search error: {e}")
            return {
                'success': False,
                'error': str(e),
                'products': [],
                'source': 'jeevee'
            }
    
    def get_products(self, category: Optional[str] = None, page: int = 1, limit: int = 20) -> Dict:
        """
        Get products from Jeevee (optionally filtered by category)
        
        Args:
            category: Category ID or slug (optional)
            page: Page number
            limit: Results per page
            
        Returns:
            Dictionary with products and metadata
        """
        try:
            url = f"{self.BASE_URL}/products?page={page}&limit={limit}"
            if category:
                url += f"&category={category}"
            
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            products = self._parse_products(data.get('data', []))
            
            return {
                'success': True,
                'products': products,
                'total': data.get('total_results', 0),
                'page': data.get('page', page),
                'total_pages': data.get('total_pages', 1),
                'source': 'jeevee'
            }
            
        except requests.RequestException as e:
            logger.error(f"Jeevee get_products error: {e}")
            return {
                'success': False,
                'error': str(e),
                'products': [],
                'source': 'jeevee'
            }
    
    def _generate_slug(self, text: str) -> str:
        """Generate URL-safe slug from product name"""
        import re
        # Convert to lowercase
        slug = text.lower()
        # Replace special characters with hyphens
        slug = re.sub(r'[^a-z0-9\s-]', '', slug)
        # Replace spaces and multiple hyphens with single hyphen
        slug = re.sub(r'[\s_]+', '-', slug)
        slug = re.sub(r'-+', '-', slug)
        # Remove leading/trailing hyphens
        slug = slug.strip('-')
        return slug
    
    def _parse_products(self, items: List[Dict]) -> List[Dict]:
        """Parse Jeevee product data into standardized format"""
        products = []
        
        for item in items:
            try:
                product = self._parse_single_product(item)
                if product:
                    products.append(product)
            except Exception as e:
                logger.warning(f"Error parsing Jeevee product: {e}")
                continue
        
        return products
    
    def _parse_single_product(self, item: Dict) -> Optional[Dict]:
        """Parse a single product item"""
        if not item:
            return None
        
        # Extract product name
        name = item.get('label', '') or f"Product {item.get('product_id', 'Unknown')}"
        
        # Extract price (current selling price)
        price = item.get('price', 0)
        
        # Calculate original price if discount exists
        discount = item.get('discount', 0)
        if discount and discount > 0:
            original_price = round(price / (1 - discount / 100), 2)
        else:
            original_price = price
        
        # Extract image URL (get medium size - 512px)
        image = ''
        images = item.get('image', [])
        if images and isinstance(images, list) and len(images) > 0:
            first_image = images[0]
            if isinstance(first_image, dict):
                # Prefer 512px size, fallback to others
                image = first_image.get('512') or first_image.get('256') or first_image.get('1024') or ''
        
        # Extract brand
        brand_info = item.get('brand', {})
        brand = brand_info.get('name', '') if isinstance(brand_info, dict) else ''
        
        # Extract rating
        rating_info = item.get('review_and_rating', {})
        rating = rating_info.get('avg_rating', 0) if rating_info else 0
        review_count = rating_info.get('review_count', 0) if rating_info else 0
        
        # Build product URL - Jeevee uses /products/{slug}-{product_id} format
        product_id = item.get('product_id', '')
        seo_details = item.get('seo_details', {})
        slug = seo_details.get('slug', '') if seo_details else ''
        
        # If no slug in SEO details, generate from label
        if not slug:
            slug = self._generate_slug(name)
        
        # Build URL with slug and product ID
        product_url = f"{self.WEBSITE_URL}/products/{slug}-{product_id}"
        
        return {
            'id': str(product_id),
            'name': name,
            'price': str(price),
            'original_price': str(original_price),
            'discount': f"{discount}%" if discount else None,
            'image': image,
            'url': product_url,
            'link': product_url,  # Alias for frontend compatibility
            'brand': brand,
            'rating': str(rating) if rating else None,
            'review_count': review_count,
            'in_stock': not item.get('sold_out', False),
            'source': 'Jeevee',
            'currency': 'NPR',
            'manufacturer': item.get('manufacturing_company', ''),
            'category': str(item.get('primary_category', '')),
        }
    
    def get_categories(self) -> Dict:
        """Get available categories from Jeevee"""
        try:
            url = f"{self.BASE_URL}/categories"
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            return {
                'success': True,
                'categories': data,
                'source': 'jeevee'
            }
        except requests.RequestException as e:
            logger.error(f"Jeevee get_categories error: {e}")
            return {
                'success': False,
                'error': str(e),
                'categories': [],
                'source': 'jeevee'
            }


# Convenience function for direct usage
def search_jeevee(query: str, page: int = 1, limit: int = 20) -> Dict:
    """
    Search for products on Jeevee
    
    Args:
        query: Search term
        page: Page number
        limit: Results per page
        
    Returns:
        Dictionary with products and metadata
    """
    scraper = JeeveeScraper()
    return scraper.search(query, page, limit)


if __name__ == "__main__":
    # Test the scraper
    scraper = JeeveeScraper()
    
    # Test search
    print("Testing Jeevee search for 'face wash'...")
    result = scraper.search("face wash", limit=5)
    
    if result['success']:
        print(f"Found {result['total']} products")
        print(f"Showing {len(result['products'])} products:\n")
        
        for i, product in enumerate(result['products'], 1):
            print(f"{i}. {product['name']}")
            print(f"   Price: NPR {product['price']}")
            print(f"   Brand: {product['brand']}")
            print(f"   Rating: {product['rating']}")
            print(f"   In Stock: {product['in_stock']}")
            print()
    else:
        print(f"Error: {result.get('error')}")
