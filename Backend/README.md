# Backend API and Scraper Setup

## Prerequisites
- Python 3.8+
- Django, djangorestframework, django-cors-headers, requests, beautifulsoup4

## Install dependencies
```bash
pip install django djangorestframework django-cors-headers requests beautifulsoup4
```

## Project Structure
```
Backend/
├── api/
│   └── views.py         # API endpoints for products, cart, scraping
├── scraper/
│   └── webscraper.py    # Web scraper for Nike, Adidas, Amazon, etc.
├── ulrs.py              # URL routing
└── README.md
```

## API Endpoints

### Products
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/products/` | Get all products (filter: ?category=, ?brand=, ?featured=) |
| GET | `/api/products/<id>/` | Get single product by ID |

### Shopping Cart
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/cart/` | Get cart items and total |
| POST | `/api/cart/` | Add item to cart `{"product_id": 1, "quantity": 1, "size": 10, "color": "#2e2c2e"}` |
| DELETE | `/api/cart/` | Remove item from cart |

### Web Scraping
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/scrape/` | Scrape products from URL `{"url": "https://..."}` |
| POST | `/api/search-shoes/` | Search shoes `{"query": "running shoes", "site": "nike"}` |

### Frontend Data
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/nav-links/` | Get navigation menu items |
| GET | `/api/performance/` | Get performance section data |
| GET | `/api/features/` | Get features data |
| POST | `/api/contact/` | Submit contact form |

## Quick Start

1. Create a Django project (if not exists):
   ```bash
   django-admin startproject config .
   ```

2. Add to `config/settings.py`:
   ```python
   INSTALLED_APPS = [
       ...
       'rest_framework',
       'corsheaders',
       'api',
       'scraper',
   ]

   MIDDLEWARE = [
       'corsheaders.middleware.CorsMiddleware',
       ...
   ]

   CORS_ALLOWED_ORIGINS = [
       "http://localhost:5173",  # Vite dev server
       "http://127.0.0.1:5173",
   ]
   ```

3. Include URLs in `config/urls.py`:
   ```python
   from django.urls import path, include
   urlpatterns = [
       path('', include('ulrs')),
   ]
   ```

4. Run the server:
   ```bash
   python manage.py runserver
   ```

## Example API Calls

### Get all products
```bash
curl http://localhost:8000/api/products/
```

### Get featured products
```bash
curl "http://localhost:8000/api/products/?featured=true"
```

### Add to cart
```bash
curl -X POST http://localhost:8000/api/cart/ \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1, "quantity": 1, "size": 10, "color": "#2e2c2e"}'
```

### Scrape Nike shoes
```bash
curl -X POST http://localhost:8000/api/scrape/ \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.nike.com/w/mens-shoes-nik1zy7ok"}'
```

### Search for shoes
```bash
curl -X POST http://localhost:8000/api/search-shoes/ \
  -H "Content-Type: application/json" \
  -d '{"query": "air max", "site": "nike"}'
```

## Supported Scraping Sites
- Nike (nike.com)
- Adidas (adidas.com)
- Amazon (amazon.com)
- Generic sites (fallback parser)

## Notes
- Extend `WebScraper` in `scraper/webscraper.py` for custom site parsers
- Replace in-memory storage with Django models for production
- Add authentication for cart/checkout in production
