from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from scraper.webscraper import WebScraper
from scraper.daraz import DarazScraper, search_daraz
from scraper.jeevee import JeeveeScraper, search_jeevee
from scraper.price_compare import PriceComparer, compare_prices, get_lowest_prices

# In-memory product storage (replace with database models in production)
PRODUCTS = [
    {
        'id': 1,
        'name': 'Nike Air Max 270',
        'price': 150.00,
        'description': 'The Nike Air Max 270 delivers visible cushioning under every step.',
        'image': '/images/shoe1.png',
        'colors': ['#2e2c2e', '#ffffff', '#ff0000', '#0000ff'],
        'sizes': [7, 8, 9, 10, 11, 12],
        'category': 'running',
        'brand': 'Nike',
        'featured': True,
    },
    {
        'id': 2,
        'name': 'Nike React Infinity',
        'price': 160.00,
        'description': 'Designed to help reduce injury and keep you on the run.',
        'image': '/images/shoe2.png',
        'colors': ['#2e2c2e', '#808080', '#00ff00'],
        'sizes': [7, 8, 9, 10, 11],
        'category': 'running',
        'brand': 'Nike',
        'featured': True,
    },
    {
        'id': 3,
        'name': 'Nike ZoomX Vaporfly',
        'price': 250.00,
        'description': 'Built for record-breaking speed.',
        'image': '/images/shoe3.png',
        'colors': ['#ff6b6b', '#4ecdc4', '#2e2c2e'],
        'sizes': [8, 9, 10, 11, 12],
        'category': 'performance',
        'brand': 'Nike',
        'featured': False,
    },
]

CART = []

# Navigation links matching frontend
NAV_LINKS = [
    {'label': 'Store'},
    {'label': 'Shoes'},
    {'label': 'About'},
    {'label': 'Features'},
    {'label': 'Vision'},
    {'label': 'Contact'},
]

# Performance images data
PERFORMANCE_DATA = [
    {'id': 'p1', 'src': '/performance1.png', 'title': 'Lightweight Design'},
    {'id': 'p2', 'src': '/performance2.png', 'title': 'Superior Cushioning'},
    {'id': 'p3', 'src': '/performance3.png', 'title': 'Breathable Mesh'},
    {'id': 'p4', 'src': '/performance4.png', 'title': 'Durable Outsole'},
    {'id': 'p5', 'src': '/performance5.jpg', 'title': 'Energy Return'},
    {'id': 'p6', 'src': '/performance6.png', 'title': 'Perfect Fit'},
    {'id': 'p7', 'src': '/performance7.png', 'title': 'All-terrain Grip'},
]

# Features data
FEATURES = [
    {
        'id': 1,
        'icon': '/feature-icon1.svg',
        'highlight': 'Comfort First.',
        'text': 'Experience all-day comfort with our advanced cushioning technology.',
    },
    {
        'id': 2,
        'icon': '/feature-icon2.svg',
        'highlight': 'Built to Last.',
        'text': 'Premium materials ensure durability through every mile.',
    },
    {
        'id': 3,
        'icon': '/feature-icon3.svg',
        'highlight': 'Style Meets Function.',
        'text': 'Sleek designs that perform as good as they look.',
    },
    {
        'id': 4,
        'icon': '/feature-icon4.svg',
        'highlight': 'Eco-Friendly.',
        'text': 'Sustainable materials for a better tomorrow.',
    },
    {
        'id': 5,
        'icon': '/feature-icon5.svg',
        'highlight': 'Custom Fit.',
        'text': 'Adaptive technology that molds to your unique foot shape.',
    },
]


class ScrapeView(APIView):
    """
    POST with {"url": "https://example.com"} to scrape product data from a site.
    """
    def post(self, request):
        url = request.data.get('url')
        if not url:
            return Response({'error': 'URL is required'}, status=status.HTTP_400_BAD_REQUEST)
        scraper = WebScraper()
        try:
            data = scraper.fetch(url)
            return Response(data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DarazSearchView(APIView):
    """
    Search products on Daraz.
    POST with {"query": "shoes", "region": "pk", "page": 1, "sort": "popularity"}
    Regions: pk (Pakistan), np (Nepal), bd (Bangladesh), lk (Sri Lanka)
    Sort: popularity, price_low, price_high, newest
    """
    def post(self, request):
        query = request.data.get('query', '')
        region = request.data.get('region', 'pk')
        page = request.data.get('page', 1)
        sort = request.data.get('sort', 'popularity')
        
        if not query:
            return Response({'error': 'Query is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            scraper = DarazScraper(region=region)
            data = scraper.search(query, page=page, sort=sort)
            return Response(data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def get(self, request):
        """GET method for easy browser testing."""
        query = request.query_params.get('q', '')
        region = request.query_params.get('region', 'pk')
        page = int(request.query_params.get('page', 1))
        
        if not query:
            return Response({'error': 'Query parameter "q" is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            scraper = DarazScraper(region=region)
            data = scraper.search(query, page=page)
            return Response(data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DarazCategoryView(APIView):
    """
    Get products from a Daraz category.
    GET /api/daraz/category/?slug=mens-shoes&region=pk&page=1
    """
    def get(self, request):
        slug = request.query_params.get('slug', '')
        region = request.query_params.get('region', 'pk')
        page = int(request.query_params.get('page', 1))
        
        if not slug:
            return Response({'error': 'Category slug is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            scraper = DarazScraper(region=region)
            data = scraper.get_category(slug, page=page)
            return Response(data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DarazDealsView(APIView):
    """Get current Daraz deals and flash sales."""
    def get(self, request):
        region = request.query_params.get('region', 'pk')
        
        try:
            scraper = DarazScraper(region=region)
            data = scraper.get_deals()
            return Response(data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DarazProductDetailView(APIView):
    """
    Get detailed product info from Daraz.
    POST with {"url": "https://www.daraz.pk/products/..."}
    """
    def post(self, request):
        url = request.data.get('url', '')
        region = request.data.get('region', 'pk')
        
        if not url:
            return Response({'error': 'Product URL is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            scraper = DarazScraper(region=region)
            data = scraper.get_product_details(url)
            return Response(data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SearchShoesView(APIView):
    """
    POST with {"query": "running shoes", "site": "nike"} to search for shoes.
    site can be: nike, adidas, amazon, or all
    """
    def post(self, request):
        query = request.data.get('query', '')
        site = request.data.get('site', 'all')
        
        if not query:
            return Response({'error': 'Query is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        scraper = WebScraper()
        try:
            data = scraper.search_shoes(query, site)
            return Response(data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProductListView(APIView):
    """Get all products or filter by category/brand."""
    def get(self, request):
        category = request.query_params.get('category')
        brand = request.query_params.get('brand')
        featured = request.query_params.get('featured')
        
        products = PRODUCTS.copy()
        
        if category:
            products = [p for p in products if p['category'] == category]
        if brand:
            products = [p for p in products if p['brand'].lower() == brand.lower()]
        if featured:
            products = [p for p in products if p['featured']]
        
        return Response({'products': products})


class ProductDetailView(APIView):
    """Get a single product by ID."""
    def get(self, request, product_id):
        product = next((p for p in PRODUCTS if p['id'] == product_id), None)
        if not product:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(product)


class CartView(APIView):
    """Manage shopping cart."""
    def get(self, request):
        total = sum(item['price'] * item['quantity'] for item in CART)
        return Response({'items': CART, 'total': total, 'count': len(CART)})
    
    def post(self, request):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)
        size = request.data.get('size')
        color = request.data.get('color')
        
        product = next((p for p in PRODUCTS if p['id'] == product_id), None)
        if not product:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        
        cart_item = {
            'product_id': product_id,
            'name': product['name'],
            'price': product['price'],
            'quantity': quantity,
            'size': size,
            'color': color,
            'image': product['image'],
        }
        
        # Check if item already in cart
        existing = next((i for i in CART if i['product_id'] == product_id and i['size'] == size and i['color'] == color), None)
        if existing:
            existing['quantity'] += quantity
        else:
            CART.append(cart_item)
        
        return Response({'message': 'Added to cart', 'cart': CART})
    
    def delete(self, request):
        product_id = request.data.get('product_id')
        size = request.data.get('size')
        color = request.data.get('color')
        
        global CART
        CART = [i for i in CART if not (i['product_id'] == product_id and i['size'] == size and i['color'] == color)]
        
        return Response({'message': 'Removed from cart', 'cart': CART})


class NavLinksView(APIView):
    """Get navigation links."""
    def get(self, request):
        return Response({'navLinks': NAV_LINKS})


class PerformanceView(APIView):
    """Get performance section data."""
    def get(self, request):
        return Response({'performanceData': PERFORMANCE_DATA})


class FeaturesView(APIView):
    """Get features data."""
    def get(self, request):
        return Response({'features': FEATURES})


class ContactView(APIView):
    """Handle contact form submissions."""
    def post(self, request):
        name = request.data.get('name')
        email = request.data.get('email')
        message = request.data.get('message')
        
        if not all([name, email, message]):
            return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # In production, save to database or send email
        return Response({'message': 'Thank you for your message! We will get back to you soon.'})


# ============== JEEVEE VIEWS ==============

class JeeveeSearchView(APIView):
    """
    Search products on Jeevee (Nepal's health & lifestyle platform).
    POST with {"query": "face wash", "page": 1, "limit": 20}
    GET with ?q=face+wash&page=1&limit=20
    """
    def post(self, request):
        query = request.data.get('query', '')
        page = request.data.get('page', 1)
        limit = request.data.get('limit', 20)
        
        if not query:
            return Response({'error': 'Query is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            scraper = JeeveeScraper()
            data = scraper.search(query, page=page, limit=limit)
            return Response(data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def get(self, request):
        """GET method for easy browser testing."""
        query = request.query_params.get('q', '')
        page = int(request.query_params.get('page', 1))
        limit = int(request.query_params.get('limit', 20))
        
        if not query:
            return Response({'error': 'Query parameter "q" is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            scraper = JeeveeScraper()
            data = scraper.search(query, page=page, limit=limit)
            return Response(data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class JeeveeProductsView(APIView):
    """
    Get products from Jeevee (optionally filtered by category).
    GET with ?category=skin-care&page=1&limit=20
    """
    def get(self, request):
        category = request.query_params.get('category', None)
        page = int(request.query_params.get('page', 1))
        limit = int(request.query_params.get('limit', 20))
        
        try:
            scraper = JeeveeScraper()
            data = scraper.get_products(category=category, page=page, limit=limit)
            return Response(data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class JeeveeCategoriesView(APIView):
    """Get available categories from Jeevee."""
    def get(self, request):
        try:
            scraper = JeeveeScraper()
            data = scraper.get_categories()
            return Response(data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ============== PRICE COMPARISON VIEWS ==============

class PriceCompareView(APIView):
    """
    Compare prices between Daraz and Jeevee.
    POST with {"query": "face wash", "limit": 20, "min_rating": 4.0}
    GET with ?q=face+wash&limit=20&min_rating=4
    
    Returns products from both platforms with price comparison data.
    Only products with rating >= min_rating are returned (default: 4.0).
    Set min_rating=0 to disable rating filter.
    """
    def post(self, request):
        query = request.data.get('query', '')
        limit = request.data.get('limit', 20)
        min_rating = request.data.get('min_rating', 4.0)  # Default: only 4+ rated products
        
        if not query:
            return Response({'error': 'Query is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Convert min_rating to float, None if 0 or not provided
            min_rating = float(min_rating) if min_rating and float(min_rating) > 0 else None
            
            comparer = PriceComparer()
            data = comparer.search_all(query, limit=limit, min_rating=min_rating)
            return Response(data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def get(self, request):
        """GET method for easy browser testing."""
        query = request.query_params.get('q', '')
        limit = int(request.query_params.get('limit', 20))
        min_rating = request.query_params.get('min_rating', '4.0')  # Default: only 4+ rated products
        
        if not query:
            return Response({'error': 'Query parameter "q" is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Convert min_rating to float, None if 0 or "0"
            min_rating = float(min_rating) if min_rating and float(min_rating) > 0 else None
            
            comparer = PriceComparer()
            data = comparer.search_all(query, limit=limit, min_rating=min_rating)
            return Response(data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LowestPricesView(APIView):
    """
    Get products sorted by lowest price across all platforms.
    POST with {"query": "face wash", "limit": 20, "min_rating": 4.0}
    GET with ?q=face+wash&limit=20&min_rating=4
    
    Returns a single list of products sorted by price (lowest first).
    Only products with rating >= min_rating are returned (default: 4.0).
    Set min_rating=0 to disable rating filter.
    """
    def post(self, request):
        query = request.data.get('query', '')
        limit = request.data.get('limit', 20)
        min_rating = request.data.get('min_rating', 4.0)  # Default: only 4+ rated products
        
        if not query:
            return Response({'error': 'Query is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Convert min_rating to float, None if 0 or not provided
            min_rating = float(min_rating) if min_rating and float(min_rating) > 0 else None
            
            comparer = PriceComparer()
            data = comparer.get_lowest_prices(query, limit=limit, min_rating=min_rating)
            return Response(data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def get(self, request):
        """GET method for easy browser testing."""
        query = request.query_params.get('q', '')
        limit = int(request.query_params.get('limit', 20))
        min_rating = request.query_params.get('min_rating', '4.0')  # Default: only 4+ rated products
        
        if not query:
            return Response({'error': 'Query parameter "q" is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Convert min_rating to float, None if 0 or "0"
            min_rating = float(min_rating) if min_rating and float(min_rating) > 0 else None
            
            comparer = PriceComparer()
            data = comparer.get_lowest_prices(query, limit=limit, min_rating=min_rating)
            return Response(data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
