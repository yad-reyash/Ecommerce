import { useState, useEffect, useCallback } from 'react';
import * as api from '../services/api';

/**
 * Hook to fetch products from backend
 */
export function useProducts(filters = {}) {
    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        api.getProducts(filters)
            .then(data => {
                setProducts(data.products || []);
                setError(null);
            })
            .catch(err => setError(err.message))
            .finally(() => setLoading(false));
    }, [JSON.stringify(filters)]);

    return { products, loading, error };
}

/**
 * Hook to manage shopping cart
 */
export function useCart() {
    const [cart, setCart] = useState({ items: [], total: 0, count: 0 });
    const [loading, setLoading] = useState(false);

    const fetchCart = async () => {
        try {
            const data = await api.getCart();
            setCart(data);
        } catch (err) {
            console.error('Failed to fetch cart:', err);
        }
    };

    const addItem = async (productId, quantity = 1, size = null, color = null) => {
        setLoading(true);
        try {
            const data = await api.addToCart(productId, quantity, size, color);
            setCart({ ...cart, items: data.cart });
            await fetchCart();
        } catch (err) {
            console.error('Failed to add to cart:', err);
        } finally {
            setLoading(false);
        }
    };

    const removeItem = async (productId, size = null, color = null) => {
        setLoading(true);
        try {
            await api.removeFromCart(productId, size, color);
            await fetchCart();
        } catch (err) {
            console.error('Failed to remove from cart:', err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchCart();
    }, []);

    return { cart, addItem, removeItem, loading, refetch: fetchCart };
}

/**
 * Hook to fetch features data
 */
export function useFeatures() {
    const [features, setFeatures] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        api.getFeatures()
            .then(data => setFeatures(data.features || []))
            .catch(err => console.error('Failed to fetch features:', err))
            .finally(() => setLoading(false));
    }, []);

    return { features, loading };
}

/**
 * Hook to fetch performance data
 */
export function usePerformance() {
    const [performanceData, setPerformanceData] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        api.getPerformanceData()
            .then(data => setPerformanceData(data.performanceData || []))
            .catch(err => console.error('Failed to fetch performance data:', err))
            .finally(() => setLoading(false));
    }, []);

    return { performanceData, loading };
}

/**
 * Hook to search/scrape shoes
 */
export function useShoeSearch() {
    const [results, setResults] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const search = async (query, site = 'all') => {
        setLoading(true);
        setError(null);
        try {
            const data = await api.searchShoes(query, site);
            setResults(data.products || []);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const scrape = async (url) => {
        setLoading(true);
        setError(null);
        try {
            const data = await api.scrapeProducts(url);
            setResults(data.products || []);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return { results, search, scrape, loading, error };
}

/**
 * Hook to search shoes on Daraz
 */
export function useDarazSearch() {
    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [pagination, setPagination] = useState({ page: 1, hasMore: true });

    const search = async (query, region = 'pk', page = 1, sort = 'popularity') => {
        setLoading(true);
        setError(null);
        try {
            const data = await api.searchDaraz(query, region, page, sort);
            if (page === 1) {
                setProducts(data.products || []);
            } else {
                setProducts(prev => [...prev, ...(data.products || [])]);
            }
            setPagination({
                page,
                hasMore: (data.products || []).length > 0,
                count: data.count,
            });
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const loadMore = async (query, region = 'pk', sort = 'popularity') => {
        if (!loading && pagination.hasMore) {
            await search(query, region, pagination.page + 1, sort);
        }
    };

    // Filter products to only show shoes
    const filterShoes = (products) => {
        const shoeKeywords = ['shoe', 'shoes', 'sneaker', 'sneakers', 'boot', 'boots', 'sandal', 'sandals', 'loafer', 'slipper', 'heel', 'flat', 'trainer', 'footwear', 'জুতা', 'जूता'];
        return products.filter(product => {
            const name = (product.name || '').toLowerCase();
            return shoeKeywords.some(keyword => name.includes(keyword.toLowerCase()));
        });
    };

    const shoes = filterShoes(products);

    return { products, shoes, search, loadMore, loading, error, pagination };
}

/**
 * Hook to get Daraz deals
 */
export function useDarazDeals(region = 'pk') {
    const [deals, setDeals] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        api.getDarazDeals(region)
            .then(data => {
                setDeals(data.products || []);
                setError(null);
            })
            .catch(err => setError(err.message))
            .finally(() => setLoading(false));
    }, [region]);

    return { deals, loading, error };
}

/**
 * Hook to search and compare prices from both Daraz and Jeevee
 */
export function usePriceCompare() {
    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [pagination, setPagination] = useState({ page: 1, hasMore: true });
    const [sources, setSources] = useState({ daraz: 0, jeevee: 0 });

    const search = useCallback(async (query, region = 'np', limit = 50) => {
        setLoading(true);
        setError(null);
        try {
            const data = await api.getLowestPrices(query, region, limit);
            const productList = data.products || [];
            setProducts(productList);
            
            // Count products by source
            const darazCount = productList.filter(p => p.source === 'Daraz').length;
            const jeeveeCount = productList.filter(p => p.source === 'Jeevee').length;
            setSources({ daraz: darazCount, jeevee: jeeveeCount });
            
            setPagination({
                page: 1,
                hasMore: productList.length >= limit,
                count: productList.length,
            });
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }, []);

    // Filter products to only show shoes
    const filterShoes = (products) => {
        const shoeKeywords = ['shoe', 'shoes', 'sneaker', 'sneakers', 'boot', 'boots', 'sandal', 'sandals', 'loafer', 'slipper', 'heel', 'flat', 'trainer', 'footwear', 'জুতা', 'जूता'];
        return products.filter(product => {
            const name = (product.name || '').toLowerCase();
            return shoeKeywords.some(keyword => name.includes(keyword.toLowerCase()));
        });
    };

    const shoes = filterShoes(products);

    return { products, shoes, search, loading, error, pagination, sources };
}

/**
 * Hook to search Jeevee products
 */
export function useJeeveeSearch() {
    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const search = useCallback(async (query, page = 1, limit = 40) => {
        setLoading(true);
        setError(null);
        try {
            const data = await api.searchJeevee(query, page, limit);
            setProducts(data.products || []);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }, []);

    return { products, search, loading, error };
}
