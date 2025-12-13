// API configuration and service
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

class ApiService {
  constructor(baseURL) {
    this.baseURL = baseURL;
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
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
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  // Products
  async getProducts(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    const endpoint = queryString ? `/products/?${queryString}` : '/products/';
    return this.request(endpoint);
  }

  async getProduct(id) {
    return this.request(`/products/${id}/`);
  }

  async getFeaturedProducts() {
    return this.request('/products/featured/');
  }

  // Categories
  async getCategories() {
    return this.request('/categories/');
  }

  async getCategory(id) {
    return this.request(`/categories/${id}/`);
  }
}

export const api = new ApiService(API_BASE_URL);
export default api;
