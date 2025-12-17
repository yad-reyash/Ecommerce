// API configuration for connecting to Django backend
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

/**
 * Fetch wrapper with error handling
 */
async function fetchAPI(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    
    const config = {
        headers: {
            'Content-Type': 'application/json',
            ...options.headers,
        },
        ...options,
    };

    try {
        const response = await fetch(url, config);
        
        if (!response.ok) {
            const error = await response.json().catch(() => ({}));
            throw new Error(error.message || `HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error(`API Error (${endpoint}):`, error);
        throw error;
    }
}

// Product APIs
export const getProducts = (params = {}) => {
    const query = new URLSearchParams(params).toString();
    return fetchAPI(`/api/products/${query ? `?${query}` : ''}`);
};

export const getProductById = (id) => {
    return fetchAPI(`/api/products/${id}/`);
};

export const getFeaturedProducts = () => {
    return fetchAPI('/api/products/?featured=true');
};

// Cart APIs
export const getCart = () => {
    return fetchAPI('/api/cart/');
};

export const addToCart = (productId, quantity = 1, size = null, color = null) => {
    return fetchAPI('/api/cart/', {
        method: 'POST',
        body: JSON.stringify({ product_id: productId, quantity, size, color }),
    });
};

export const removeFromCart = (productId, size = null, color = null) => {
    return fetchAPI('/api/cart/', {
        method: 'DELETE',
        body: JSON.stringify({ product_id: productId, size, color }),
    });
};

// Navigation & UI Data APIs
export const getNavLinks = () => {
    return fetchAPI('/api/nav-links/');
};

export const getPerformanceData = () => {
    return fetchAPI('/api/performance/');
};

export const getFeatures = () => {
    return fetchAPI('/api/features/');
};

// Scraper APIs
export const scrapeProducts = (url) => {
    return fetchAPI('/api/scrape/', {
        method: 'POST',
        body: JSON.stringify({ url }),
    });
};

export const searchShoes = (query, site = 'all') => {
    return fetchAPI('/api/search-shoes/', {
        method: 'POST',
        body: JSON.stringify({ query, site }),
    });
};

// Contact API
export const submitContact = (name, email, message) => {
    return fetchAPI('/api/contact/', {
        method: 'POST',
        body: JSON.stringify({ name, email, message }),
    });
};

// Daraz Scraper APIs
export const searchDaraz = (query, region = 'pk', page = 1, sort = 'popularity') => {
    return fetchAPI('/api/daraz/search/', {
        method: 'POST',
        body: JSON.stringify({ query, region, page, sort }),
    });
};

export const searchDarazGet = (query, region = 'pk', page = 1) => {
    return fetchAPI(`/api/daraz/search/?q=${encodeURIComponent(query)}&region=${region}&page=${page}`);
};

export const getDarazCategory = (slug, region = 'pk', page = 1) => {
    return fetchAPI(`/api/daraz/category/?slug=${encodeURIComponent(slug)}&region=${region}&page=${page}`);
};

export const getDarazDeals = (region = 'pk') => {
    return fetchAPI(`/api/daraz/deals/?region=${region}`);
};

export const getDarazProductDetails = (url, region = 'pk') => {
    return fetchAPI('/api/daraz/product/', {
        method: 'POST',
        body: JSON.stringify({ url, region }),
    });
};

// Jeevee Scraper APIs
export const searchJeevee = (query, page = 1, limit = 40) => {
    return fetchAPI(`/api/jeevee/search/?q=${encodeURIComponent(query)}&page=${page}&limit=${limit}`);
};

export const getJeeveeProducts = (page = 1, limit = 40) => {
    return fetchAPI(`/api/jeevee/products/?page=${page}&limit=${limit}`);
};

export const getJeeveeCategories = () => {
    return fetchAPI('/api/jeevee/categories/');
};

// Price Comparison APIs
export const compareAllPrices = (query, region = 'np') => {
    return fetchAPI(`/api/compare/?q=${encodeURIComponent(query)}&region=${region}`);
};

export const getLowestPrices = (query, region = 'np', limit = 50) => {
    return fetchAPI(`/api/lowest-prices/?q=${encodeURIComponent(query)}&region=${region}&limit=${limit}`);
};

export default {
    getProducts,
    getProductById,
    getFeaturedProducts,
    getCart,
    addToCart,
    removeFromCart,
    getNavLinks,
    getPerformanceData,
    getFeatures,
    scrapeProducts,
    searchShoes,
    submitContact,
    searchDaraz,
    searchDarazGet,
    getDarazCategory,
    getDarazDeals,
    getDarazProductDetails,
    searchJeevee,
    getJeeveeProducts,
    getJeeveeCategories,
    compareAllPrices,
    getLowestPrices,
};
