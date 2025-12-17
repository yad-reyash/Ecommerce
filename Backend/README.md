# 🔧 Backend API - Nepal Price Comparison

Django REST API backend for scraping and comparing prices from Daraz and Jeevee Nepal.

---

## 📁 Structure

```
Backend/
├── api/
│   ├── views.py           # API endpoints
│   └── serializers.py     # Data serializers
├── scraper/
│   ├── daraz.py           # Daraz Nepal scraper (Selenium)
│   ├── jeevee.py          # Jeevee Nepal API
│   └── price_compare.py   # Price comparison logic
├── config/
│   ├── settings.py        # Django settings
│   └── urls.py            # URL routing
├── manage.py
└── requirements.txt
```

---

## 🚀 Setup

### 1. Create Virtual Environment

```bash
python -m venv venv

# Windows
.\venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt

# If Python 3.12+ (distutils error):
pip install setuptools
```

### 3. Run Server

```bash
python manage.py runserver 0.0.0.0:8000
```

Server runs at: **http://127.0.0.1:8000**

---

## 📡 API Endpoints

### Price Comparison

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/lowest-prices/` | Compare prices from all sources |

**Query Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `q` | string | required | Search query |
| `region` | string | `np` | Region code |
| `limit` | int | `50` | Max results per source |
| `min_rating` | float | `0` | Minimum rating |

**Example Request:**
```bash
curl "http://127.0.0.1:8000/api/lowest-prices/?q=moisturizer&limit=20"
```

**Example Response:**
```json
{
    "success": true,
    "query": "moisturizer",
    "total": 15,
    "products": [
        {
            "name": "Cetaphil Moisturizing Cream",
            "price": "Rs. 1,200",
            "original_price": "Rs. 1,500",
            "discount": "20%",
            "rating": "4.5",
            "image": "https://...",
            "url": "https://...",
            "source": "Jeevee"
        }
    ]
}
```

### Products & Cart

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/products/` | Get all products |
| `GET` | `/api/products/<id>/` | Get single product |
| `GET` | `/api/cart/` | Get cart items |
| `POST` | `/api/cart/` | Add to cart |
| `DELETE` | `/api/cart/` | Remove from cart |

---

## 🕷️ Scrapers

### Daraz Scraper (`scraper/daraz.py`)

Uses Selenium with undetected-chromedriver to bypass anti-bot protection.

```python
from scraper.daraz import DarazScraper

scraper = DarazScraper()
products = scraper.search("phone", limit=20)
```

**Features:**
- Headless Chrome browser
- Anti-bot bypass
- Multiple CSS selectors for resilience
- Graceful error handling

### Jeevee Scraper (`scraper/jeevee.py`)

Uses direct API calls to Jeevee's public API.

```python
from scraper.jeevee import JeeveeScraper

scraper = JeeveeScraper()
products = scraper.search("moisturizer", limit=20)
```

**Features:**
- Fast API-based fetching
- No browser required
- Reliable results

### Price Compare (`scraper/price_compare.py`)

Aggregates results from all scrapers.

```python
from scraper.price_compare import PriceCompare

compare = PriceCompare()
results = compare.search("laptop", min_rating=4.0)
```

---

## ⚙️ Configuration

### CORS Settings (`config/settings.py`)

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

CORS_ALLOW_ALL_ORIGINS = True  # Development only
```

### Installed Apps

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'api',
]
```

---

## 🐛 Troubleshooting

### `ModuleNotFoundError: No module named 'distutils'`
```bash
pip install setuptools
```

### Selenium ChromeDriver issues
```bash
pip install --upgrade selenium undetected-chromedriver
```

### Daraz blocking requests
- This is expected due to anti-bot protection
- The API returns graceful error message
- Jeevee results will still work

### Port already in use
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <pid> /F

# Linux/Mac
lsof -i :8000
kill -9 <pid>
```

---

## 📦 Requirements

```
django>=5.0
djangorestframework>=3.14
django-cors-headers>=4.3
requests>=2.31
beautifulsoup4>=4.12
selenium>=4.15
undetected-chromedriver>=3.5
```

---

## 🧪 Testing

```bash
# Test scrapers
python test_scrapers.py

# Test API endpoint
curl "http://127.0.0.1:8000/api/lowest-prices/?q=test"
```

---

## 📄 License

Educational project - 5th Semester
