from rest_framework import routers
from django.urls import path, include
from api import views as api_views

router = routers.DefaultRouter()

urlpatterns = [
    path('api/', include(router.urls)),
    
    # Scraping endpoints
    path('api/scrape/', api_views.ScrapeView.as_view(), name='scrape'),
    path('api/search-shoes/', api_views.SearchShoesView.as_view(), name='search-shoes'),
    
    # Daraz API endpoints (Nepal focus)
    path('api/daraz/search/', api_views.DarazSearchView.as_view(), name='daraz-search'),
    path('api/daraz/category/', api_views.DarazCategoryView.as_view(), name='daraz-category'),
    path('api/daraz/deals/', api_views.DarazDealsView.as_view(), name='daraz-deals'),
    path('api/daraz/product/', api_views.DarazProductDetailView.as_view(), name='daraz-product'),
    
    # Jeevee API endpoints (Nepal only)
    path('api/jeevee/search/', api_views.JeeveeSearchView.as_view(), name='jeevee-search'),
    path('api/jeevee/products/', api_views.JeeveeProductsView.as_view(), name='jeevee-products'),
    path('api/jeevee/categories/', api_views.JeeveeCategoriesView.as_view(), name='jeevee-categories'),
    
    # Price Comparison endpoints (Daraz vs Jeevee)
    path('api/compare/', api_views.PriceCompareView.as_view(), name='price-compare'),
    path('api/lowest-prices/', api_views.LowestPricesView.as_view(), name='lowest-prices'),
    
    # Product endpoints
    path('api/products/', api_views.ProductListView.as_view(), name='product-list'),
    path('api/products/<int:product_id>/', api_views.ProductDetailView.as_view(), name='product-detail'),
    
    # Cart endpoints
    path('api/cart/', api_views.CartView.as_view(), name='cart'),
    
    # Frontend data endpoints
    path('api/nav-links/', api_views.NavLinksView.as_view(), name='nav-links'),
    path('api/performance/', api_views.PerformanceView.as_view(), name='performance'),
    path('api/features/', api_views.FeaturesView.as_view(), name='features'),
    
    # Contact
    path('api/contact/', api_views.ContactView.as_view(), name='contact'),
]
