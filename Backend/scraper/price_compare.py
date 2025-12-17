"""
Price Comparison Module
Compares prices between Daraz and Jeevee to find the best deals
"""

import logging
from typing import Dict, List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from difflib import SequenceMatcher

from .daraz import DarazScraper
from .jeevee import JeeveeScraper

logger = logging.getLogger(__name__)


def parse_rating(rating_value) -> Optional[float]:
    """
    Parse rating from various formats to float.
    Returns None if rating cannot be parsed.
    """
    if rating_value is None:
        return None
    try:
        if isinstance(rating_value, (int, float)):
            return float(rating_value)
        # Handle string ratings like "4.5", "4.5/5", "4.5 out of 5"
        rating_str = str(rating_value).strip()
        # Extract first number
        import re
        match = re.search(r'(\d+\.?\d*)', rating_str)
        if match:
            return float(match.group(1))
        return None
    except (ValueError, TypeError):
        return None


def filter_by_rating(products: List[Dict], min_rating: float = 4.0) -> List[Dict]:
    """
    Filter products to only include those with rating >= min_rating.
    Products without ratings are excluded.
    
    Args:
        products: List of product dictionaries
        min_rating: Minimum rating threshold (default 4.0)
        
    Returns:
        Filtered list of products with rating >= min_rating
    """
    filtered = []
    for product in products:
        rating = parse_rating(product.get('rating'))
        if rating is not None and rating >= min_rating:
            product['parsed_rating'] = rating  # Add parsed rating for convenience
            filtered.append(product)
    return filtered


class PriceComparer:
    """
    Compare prices between multiple e-commerce platforms
    Currently supports: Daraz (Nepal) and Jeevee
    """
    
    def __init__(self):
        self.daraz_scraper = DarazScraper(region='np')  # Nepal
        self.jeevee_scraper = JeeveeScraper()
    
    def search_all(self, query: str, limit: int = 20, min_rating: float = None) -> Dict:
        """
        Search for products on all platforms simultaneously
        
        Args:
            query: Search term
            limit: Max results per platform
            min_rating: Minimum rating filter (e.g., 4.0 for 4+ stars). None = no filter
            
        Returns:
            Dictionary with products from all sources
        """
        results = {
            'query': query,
            'daraz': {'products': [], 'success': False},
            'jeevee': {'products': [], 'success': False},
            'all_products': [],
            'compared_products': [],
            'min_rating_filter': min_rating,
        }
        
        # Search both platforms in parallel
        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = {
                executor.submit(self._search_daraz, query, limit): 'daraz',
                executor.submit(self._search_jeevee, query, limit): 'jeevee',
            }
            
            for future in as_completed(futures):
                source = futures[future]
                try:
                    data = future.result()
                    results[source] = data
                    # Check for products - success may not always be set
                    if data.get('products'):
                        results['all_products'].extend(data['products'])
                except Exception as e:
                    logger.error(f"Error fetching from {source}: {e}")
                    results[source] = {'products': [], 'success': False, 'error': str(e)}
        
        # Apply rating filter if specified
        if min_rating is not None:
            results['all_products'] = filter_by_rating(results['all_products'], min_rating)
            results['daraz']['products'] = filter_by_rating(results['daraz'].get('products', []), min_rating)
            results['jeevee']['products'] = filter_by_rating(results['jeevee'].get('products', []), min_rating)
        
        # Sort all products by price
        results['all_products'] = self._sort_by_price(results['all_products'])
        
        # Try to match similar products for comparison
        results['compared_products'] = self._compare_products(
            results['daraz'].get('products', []),
            results['jeevee'].get('products', [])
        )
        
        return results
    
    def _search_daraz(self, query: str, limit: int) -> Dict:
        """Search Daraz for products"""
        try:
            result = self.daraz_scraper.search(query)
            products = result.get('products', [])[:limit]
            
            # Add source identifier to each product
            for p in products:
                p['source'] = 'Daraz'
                p['currency'] = 'NPR'
            
            # Success is True if we got products
            has_products = len(products) > 0
            
            return {
                'success': has_products,
                'products': products,
                'total': result.get('total', len(products)),
                'source': 'Daraz'
            }
        except Exception as e:
            logger.error(f"Daraz search error: {e}")
            return {'success': False, 'products': [], 'error': str(e)}
    
    def _search_jeevee(self, query: str, limit: int) -> Dict:
        """Search Jeevee for products"""
        try:
            result = self.jeevee_scraper.search(query, limit=limit)
            return result
        except Exception as e:
            logger.error(f"Jeevee search error: {e}")
            return {'success': False, 'products': [], 'error': str(e)}
    
    def _sort_by_price(self, products: List[Dict]) -> List[Dict]:
        """Sort products by price (lowest first)"""
        def get_price(product):
            try:
                price_str = str(product.get('price', '0'))
                # Remove currency symbols and commas
                price_str = price_str.replace(',', '').replace('Rs.', '').replace('NPR', '').strip()
                return float(price_str)
            except (ValueError, TypeError):
                return float('inf')
        
        return sorted(products, key=get_price)
    
    def _compare_products(self, daraz_products: List[Dict], jeevee_products: List[Dict]) -> List[Dict]:
        """
        Try to match similar products from both platforms
        Returns products with price comparison data
        """
        compared = []
        used_jeevee = set()
        
        for daraz_product in daraz_products:
            daraz_name = daraz_product.get('name', '').lower()
            best_match = None
            best_score = 0
            best_idx = -1
            
            for idx, jeevee_product in enumerate(jeevee_products):
                if idx in used_jeevee:
                    continue
                    
                jeevee_name = jeevee_product.get('name', '').lower()
                
                # Calculate similarity score
                score = self._similarity_score(daraz_name, jeevee_name)
                
                if score > best_score and score > 0.5:  # Minimum 50% similarity
                    best_score = score
                    best_match = jeevee_product
                    best_idx = idx
            
            comparison = {
                'daraz': daraz_product,
                'jeevee': best_match,
                'match_score': round(best_score * 100, 1),
                'has_match': best_match is not None,
            }
            
            if best_match:
                used_jeevee.add(best_idx)
                comparison['price_comparison'] = self._calculate_price_comparison(
                    daraz_product, best_match
                )
            
            compared.append(comparison)
        
        # Add unmatched Jeevee products
        for idx, jeevee_product in enumerate(jeevee_products):
            if idx not in used_jeevee:
                compared.append({
                    'daraz': None,
                    'jeevee': jeevee_product,
                    'match_score': 0,
                    'has_match': False,
                })
        
        return compared
    
    def _similarity_score(self, str1: str, str2: str) -> float:
        """Calculate similarity between two strings"""
        # Clean strings
        str1 = ' '.join(str1.split()).lower()
        str2 = ' '.join(str2.split()).lower()
        
        return SequenceMatcher(None, str1, str2).ratio()
    
    def _calculate_price_comparison(self, product1: Dict, product2: Dict) -> Dict:
        """Calculate price comparison between two products"""
        def parse_price(p):
            try:
                price_str = str(p.get('price', '0'))
                price_str = price_str.replace(',', '').replace('Rs.', '').replace('NPR', '').strip()
                return float(price_str)
            except (ValueError, TypeError):
                return None
        
        price1 = parse_price(product1)
        price2 = parse_price(product2)
        
        result = {
            'daraz_price': price1,
            'jeevee_price': price2,
            'cheaper_source': None,
            'price_difference': None,
            'percentage_difference': None,
        }
        
        if price1 is not None and price2 is not None:
            diff = abs(price1 - price2)
            result['price_difference'] = round(diff, 2)
            
            if price1 < price2:
                result['cheaper_source'] = 'daraz'
                result['percentage_difference'] = round((diff / price2) * 100, 1)
            elif price2 < price1:
                result['cheaper_source'] = 'jeevee'
                result['percentage_difference'] = round((diff / price1) * 100, 1)
            else:
                result['cheaper_source'] = 'same'
                result['percentage_difference'] = 0
        
        return result
    
    def get_lowest_prices(self, query: str, limit: int = 20, min_rating: float = None) -> Dict:
        """
        Search all platforms and return products sorted by lowest price
        
        Args:
            query: Search term
            limit: Max results to return
            min_rating: Minimum rating filter (e.g., 4.0 for 4+ stars). None = no filter
            
        Returns:
            Dictionary with sorted products by price
        """
        results = self.search_all(query, limit, min_rating=min_rating)
        
        all_products = results['all_products'][:limit]
        
        return {
            'query': query,
            'success': True,
            'products': all_products,
            'total': len(all_products),
            'min_rating_filter': min_rating,
            'sources': {
                'daraz': {
                    'success': results['daraz'].get('success', False),
                    'count': len(results['daraz'].get('products', [])),
                },
                'jeevee': {
                    'success': results['jeevee'].get('success', False),
                    'count': len(results['jeevee'].get('products', [])),
                },
            }
        }


def compare_prices(query: str, limit: int = 20, min_rating: float = None) -> Dict:
    """
    Convenience function to compare prices across platforms
    
    Args:
        query: Search term
        limit: Max results per platform
        min_rating: Minimum rating filter (e.g., 4.0 for 4+ stars)
        
    Returns:
        Dictionary with comparison results
    """
    comparer = PriceComparer()
    return comparer.search_all(query, limit, min_rating=min_rating)


def get_lowest_prices(query: str, limit: int = 20, min_rating: float = None) -> Dict:
    """
    Get products sorted by lowest price across all platforms
    
    Args:
        query: Search term
        limit: Max results
        min_rating: Minimum rating filter (e.g., 4.0 for 4+ stars)
        
    Returns:
        Dictionary with products sorted by price
    """
    comparer = PriceComparer()
    return comparer.get_lowest_prices(query, limit, min_rating=min_rating)


if __name__ == "__main__":
    # Test price comparison
    print("Testing price comparison for 'face wash'...")
    
    comparer = PriceComparer()
    result = comparer.get_lowest_prices("face wash", limit=10)
    
    print(f"\nFound {result['total']} products (sorted by price):")
    print(f"Daraz: {result['sources']['daraz']['count']} products")
    print(f"Jeevee: {result['sources']['jeevee']['count']} products")
    print()
    
    for i, product in enumerate(result['products'][:10], 1):
        source = product.get('source', 'unknown').upper()
        name = product.get('name', 'Unknown')[:50]
        price = product.get('price', 'N/A')
        print(f"{i}. [{source}] {name} - NPR {price}")
