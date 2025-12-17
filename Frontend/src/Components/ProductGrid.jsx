import { useState, useEffect, forwardRef, useImperativeHandle, useRef } from 'react';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

const ProductGrid = forwardRef((props, ref) => {
    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [searchQuery, setSearchQuery] = useState('');
    const [inputValue, setInputValue] = useState('');
    const [sourceFilter, setSourceFilter] = useState('all');
    const [sources, setSources] = useState({ daraz: 0, jeevee: 0 });
    const initialSearchDone = useRef(false);

    // Fetch products from API
    const fetchProducts = async (query = 'moisturizer') => {
        setLoading(true);
        setError(null);
        setSearchQuery(query);
        
        try {
            const url = `${API_BASE_URL}/api/lowest-prices/?q=${encodeURIComponent(query)}&region=np&limit=50&min_rating=0`;
            console.log('Fetching:', url);
            
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            console.log('API Response:', data);
            
            const productList = data.products || [];
            setProducts(productList);
            
            // Count products by source
            const darazCount = productList.filter(p => p.source === 'Daraz').length;
            const jeeveeCount = productList.filter(p => p.source === 'Jeevee').length;
            setSources({ daraz: darazCount, jeevee: jeeveeCount });
            
        } catch (err) {
            console.error('Fetch error:', err);
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    // Expose search function to parent via ref
    useImperativeHandle(ref, () => ({
        performSearch: (query) => {
            setInputValue(query);
            fetchProducts(query);
        }
    }));

    // Initial search on component mount
    useEffect(() => {
        if (!initialSearchDone.current) {
            initialSearchDone.current = true;
            fetchProducts('moisturizer');
        }
    }, []);

    // Handle search submit
    const handleSearch = (e) => {
        e.preventDefault();
        if (inputValue.trim()) {
            fetchProducts(inputValue.trim());
        }
    };

    // Filter products by source
    const filteredProducts = sourceFilter === 'all' 
        ? products 
        : products.filter(p => p.source?.toLowerCase() === sourceFilter);

    return (
        <section id="products" className="min-h-screen bg-gradient-to-b from-gray-900 to-black text-white py-16 px-4 md:px-8">
            <div className="max-w-7xl mx-auto">
                {/* Header */}
                <div className="text-center mb-12">
                    <h2 className="text-4xl md:text-6xl font-bold mb-4">
                        🛒 Compare <span className="text-transparent bg-clip-text bg-gradient-to-r from-orange-400 to-pink-500">Prices</span>
                    </h2>
                    <p className="text-gray-400 text-lg mb-8">
                        Find the best deals from Daraz & Jeevee Nepal
                    </p>
                    
                    {/* Search Box */}
                    <form onSubmit={handleSearch} className="max-w-2xl mx-auto mb-8">
                        <div className="relative flex gap-2">
                            <input
                                type="text"
                                value={inputValue}
                                onChange={(e) => setInputValue(e.target.value)}
                                placeholder="Search products... (e.g., moisturizer, phone, shoes)"
                                className="w-full px-6 py-4 bg-gray-800/50 border border-gray-700 rounded-full text-white placeholder-gray-500 focus:outline-none focus:border-orange-500 focus:ring-2 focus:ring-orange-500/20 transition-all"
                            />
                            <button
                                type="submit"
                                disabled={loading}
                                className="px-8 py-4 bg-gradient-to-r from-orange-500 to-pink-500 hover:from-orange-600 hover:to-pink-600 text-white font-bold rounded-full transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
                            >
                                {loading ? (
                                    <div className="animate-spin rounded-full h-5 w-5 border-2 border-white border-t-transparent"></div>
                                ) : (
                                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                                    </svg>
                                )}
                                Search
                            </button>
                        </div>
                    </form>

                    {/* Quick Search Tags */}
                    <div className="flex flex-wrap justify-center gap-2 mb-8">
                        {['moisturizer', 'phone', 'shoes', 'laptop', 'skincare', 'earphone'].map(tag => (
                            <button
                                key={tag}
                                onClick={() => {
                                    setInputValue(tag);
                                    fetchProducts(tag);
                                }}
                                className="px-4 py-2 bg-gray-800/50 hover:bg-orange-500/20 border border-gray-700 hover:border-orange-500 rounded-full text-sm text-gray-400 hover:text-orange-400 transition-all capitalize"
                            >
                                {tag}
                            </button>
                        ))}
                    </div>

                    {/* Current Search */}
                    {searchQuery && (
                        <p className="text-orange-400 text-lg">
                            Results for: <span className="font-bold">"{searchQuery}"</span>
                        </p>
                    )}
                </div>

                {/* Filters & Stats Row */}
                <div className="flex flex-wrap gap-4 justify-between items-center mb-8 p-4 bg-gray-800/30 rounded-2xl backdrop-blur-sm">
                    {/* Source Filter */}
                    <div className="flex gap-2">
                        {[
                            { value: 'all', label: 'All Sources', count: products.length },
                            { value: 'daraz', label: 'Daraz', count: sources.daraz, color: 'orange' },
                            { value: 'jeevee', label: 'Jeevee', count: sources.jeevee, color: 'green' },
                        ].map(({ value, label, count, color }) => (
                            <button
                                key={value}
                                onClick={() => setSourceFilter(value)}
                                className={`px-4 py-2 rounded-full text-sm font-medium transition-all ${
                                    sourceFilter === value
                                        ? color === 'orange' 
                                            ? 'bg-orange-500 text-white' 
                                            : color === 'green'
                                                ? 'bg-green-500 text-white'
                                                : 'bg-gradient-to-r from-orange-500 to-green-500 text-white'
                                        : 'bg-gray-700/50 text-gray-400 hover:bg-gray-700'
                                }`}
                            >
                                {label} ({count})
                            </button>
                        ))}
                    </div>

                    {/* Results Count */}
                    <div className="text-gray-400">
                        Showing <span className="text-white font-bold">{filteredProducts.length}</span> products
                    </div>
                </div>

                {/* Error Message */}
                {error && (
                    <div className="text-center mb-8 p-6 bg-red-500/10 border border-red-500/30 rounded-2xl">
                        <div className="text-red-400 text-lg mb-2">⚠️ Error loading products</div>
                        <p className="text-red-300/70">{error}</p>
                        <button
                            onClick={() => fetchProducts(searchQuery || 'moisturizer')}
                            className="mt-4 px-6 py-2 bg-red-500/20 hover:bg-red-500/30 text-red-400 rounded-full transition-colors"
                        >
                            Try Again
                        </button>
                    </div>
                )}

                {/* Loading State */}
                {loading && (
                    <div className="flex flex-col justify-center items-center py-20">
                        <div className="relative">
                            <div className="animate-spin rounded-full h-16 w-16 border-4 border-gray-700"></div>
                            <div className="absolute inset-0 animate-spin rounded-full h-16 w-16 border-4 border-orange-500 border-t-transparent"></div>
                        </div>
                        <p className="text-gray-400 mt-6 animate-pulse">Searching best prices...</p>
                    </div>
                )}

                {/* Product Grid */}
                {!loading && filteredProducts.length > 0 && (
                    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
                        {filteredProducts.map((product, index) => (
                            <ProductCard key={product.id || `${product.source}-${index}`} product={product} />
                        ))}
                    </div>
                )}

                {/* Empty State */}
                {!loading && !error && filteredProducts.length === 0 && (
                    <div className="text-center py-20">
                        <div className="text-8xl mb-6">🔍</div>
                        <h3 className="text-2xl font-bold mb-3">No products found</h3>
                        <p className="text-gray-400 mb-6">Try searching for something else</p>
                        <button
                            onClick={() => {
                                setInputValue('moisturizer');
                                fetchProducts('moisturizer');
                            }}
                            className="px-6 py-3 bg-orange-500 hover:bg-orange-600 text-white font-medium rounded-full transition-colors"
                        >
                            Search "moisturizer"
                        </button>
                    </div>
                )}
            </div>
        </section>
    );
});

// Product Card Component
const ProductCard = ({ product }) => {
    const [imageError, setImageError] = useState(false);
    const [imageLoaded, setImageLoaded] = useState(false);

    const formatPrice = (price) => {
        if (!price) return 'Price N/A';
        const numPrice = parseFloat(String(price).replace(/[^0-9.]/g, ''));
        if (isNaN(numPrice)) return price;
        return `Rs. ${numPrice.toLocaleString('en-NP')}`;
    };

    const getDiscount = () => {
        if (product.discount) {
            const discountVal = String(product.discount).replace('%', '');
            return parseFloat(discountVal) > 0 ? `-${Math.round(parseFloat(discountVal))}%` : null;
        }
        if (product.original_price && product.price) {
            const original = parseFloat(String(product.original_price).replace(/[^0-9.]/g, ''));
            const current = parseFloat(String(product.price).replace(/[^0-9.]/g, ''));
            if (original && current && original > current) {
                const discount = Math.round(((original - current) / original) * 100);
                return `-${discount}%`;
            }
        }
        return null;
    };

    const discount = getDiscount();
    const isJeevee = product.source === 'Jeevee';
    const sourceColor = isJeevee ? 'from-green-500 to-emerald-600' : 'from-orange-500 to-red-500';
    const sourceBgColor = isJeevee ? 'bg-green-500' : 'bg-orange-500';

    return (
        <div className="group bg-gray-800/50 backdrop-blur-sm rounded-2xl overflow-hidden border border-gray-700/50 hover:border-orange-500/50 transition-all duration-500 hover:shadow-xl hover:shadow-orange-500/10 hover:-translate-y-1">
            {/* Image Container */}
            <div className="relative aspect-square bg-gray-900 overflow-hidden">
                {!imageError && product.image ? (
                    <>
                        {!imageLoaded && (
                            <div className="absolute inset-0 bg-gray-800 animate-pulse flex items-center justify-center">
                                <div className="w-10 h-10 border-2 border-gray-600 border-t-orange-500 rounded-full animate-spin"></div>
                            </div>
                        )}
                        <img
                            src={product.image}
                            alt={product.name || 'Product'}
                            className={`w-full h-full object-cover group-hover:scale-110 transition-transform duration-700 ${imageLoaded ? 'opacity-100' : 'opacity-0'}`}
                            onLoad={() => setImageLoaded(true)}
                            onError={() => setImageError(true)}
                            loading="lazy"
                        />
                    </>
                ) : (
                    <div className="w-full h-full flex items-center justify-center bg-gradient-to-br from-gray-800 to-gray-900">
                        <svg className="w-16 h-16 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                        </svg>
                    </div>
                )}

                {/* Source Badge */}
                <div className={`absolute top-3 right-3 ${sourceBgColor} text-white text-xs font-bold px-3 py-1.5 rounded-full shadow-lg`}>
                    {product.source || 'Store'}
                </div>

                {/* Discount Badge */}
                {discount && (
                    <div className="absolute top-3 left-3 bg-red-500 text-white text-xs font-bold px-3 py-1.5 rounded-full shadow-lg animate-pulse">
                        {discount}
                    </div>
                )}

                {/* Hover Overlay */}
                <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/40 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-end justify-center pb-6">
                    {(product.link || product.url) && (
                        <a
                            href={product.url || product.link}
                            target="_blank"
                            rel="noopener noreferrer"
                            className={`px-6 py-2.5 bg-gradient-to-r ${sourceColor} hover:shadow-lg text-white text-sm font-bold rounded-full transition-all duration-300 transform hover:scale-105`}
                        >
                            View on {product.source}
                        </a>
                    )}
                </div>
            </div>

            {/* Product Info */}
            <div className="p-4">
                {/* Product Name */}
                <h3 className="text-white font-medium text-sm line-clamp-2 mb-3 min-h-[40px] group-hover:text-orange-400 transition-colors">
                    {product.name || 'Unknown Product'}
                </h3>

                {/* Price Section */}
                <div className="flex items-baseline gap-2 mb-2">
                    <span className={`font-bold text-xl bg-gradient-to-r ${sourceColor} bg-clip-text text-transparent`}>
                        {formatPrice(product.price)}
                    </span>
                </div>
                
                {product.original_price && product.original_price !== product.price && (
                    <div className="text-gray-500 text-sm line-through">
                        {formatPrice(product.original_price)}
                    </div>
                )}

                {/* Rating */}
                {product.rating && (
                    <div className="flex items-center gap-1 mt-3 text-sm">
                        <div className="flex">
                            {[...Array(5)].map((_, i) => (
                                <span key={i} className={i < Math.round(parseFloat(product.rating)) ? 'text-yellow-400' : 'text-gray-600'}>
                                    ★
                                </span>
                            ))}
                        </div>
                        <span className="text-gray-400 ml-1">{product.rating}</span>
                    </div>
                )}

                {/* Brand */}
                {product.brand && (
                    <div className="text-gray-500 text-xs mt-2 truncate">
                        {product.brand}
                    </div>
                )}
            </div>
        </div>
    );
};

ProductGrid.displayName = 'ProductGrid';

export default ProductGrid;
