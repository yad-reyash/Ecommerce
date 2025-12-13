# E-commerce Setup Guide

## Quick Start

### Option 1: Automated Setup (Recommended)

Run the setup script to install all dependencies:

```bash
chmod +x setup.sh
./setup.sh
```

Then run both servers:

```bash
chmod +x run.sh
./run.sh
```

### Option 2: Manual Setup

#### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Linux/Mac
# OR
venv\Scripts\activate  # On Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create superuser (optional):
```bash
python manage.py createsuperuser
```

6. Start backend server:
```bash
python manage.py runserver
```

#### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start development server:
```bash
npm run dev
```

## Project Structure

```
Ecommerce/
├── backend/
│   ├── ecommerce_backend/    # Django project settings
│   ├── products/             # Product catalog API
│   ├── cart/                 # Shopping cart functionality
│   ├── orders/               # Order management
│   ├── users/                # User authentication
│   ├── requirements.txt      # Python dependencies
│   └── manage.py             # Django management
│
├── frontend/
│   ├── src/                  # React source code
│   │   ├── Components/       # React components
│   │   ├── services/         # API service layer
│   │   └── store/            # State management
│   ├── public/               # Static assets
│   └── package.json          # Node dependencies
│
├── setup.sh                  # Automated setup script
├── run.sh                    # Run both servers
└── README.md                 # Main documentation
```

## API Endpoints

### Products
- `GET /api/products/` - List all products
- `GET /api/products/{id}/` - Get product details
- `GET /api/products/featured/` - Get featured products

### Categories
- `GET /api/categories/` - List all categories
- `GET /api/categories/{id}/` - Get category details

### Admin Panel
- `/admin/` - Django admin interface

## Environment Variables

### Backend (.env)
Create a `.env` file in the `backend/` directory:
```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Frontend (.env)
Create a `.env` file in the `frontend/` directory:
```env
VITE_API_URL=http://localhost:8000/api
```

## Development Workflow

1. Start backend server (runs on http://localhost:8000)
2. Start frontend server (runs on http://localhost:5173)
3. Access frontend at http://localhost:5173
4. Access backend API at http://localhost:8000/api
5. Access admin panel at http://localhost:8000/admin

## Testing

### Backend Tests
```bash
cd backend
python manage.py test
```

### Frontend Tests
```bash
cd frontend
npm run lint
npm run build
```

## Troubleshooting

### Port already in use
If you get a port conflict error:
```bash
# For backend (port 8000)
lsof -ti:8000 | xargs kill -9

# For frontend (port 5173)
lsof -ti:5173 | xargs kill -9
```

### Virtual environment issues
Make sure to activate the virtual environment before running Django commands:
```bash
cd backend
source venv/bin/activate
```

### Node modules issues
If you have frontend dependency issues:
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

## Technology Stack

**Backend:**
- Django 5.0
- Django REST Framework 3.14
- django-cors-headers 4.3
- SQLite (development database)

**Frontend:**
- React 19
- Vite 7.2
- TailwindCSS 4.1
- GSAP (animations)

## Next Steps

1. Add authentication system
2. Implement shopping cart functionality
3. Create order management system
4. Add payment integration
5. Deploy to production

## Support

For issues or questions, please create an issue in the repository.
