import { useState, useEffect, useRef } from 'react';

const SearchModal = ({ isOpen, onClose, onSearch, loading }) => {
    const [query, setQuery] = useState('');
    const inputRef = useRef(null);

    useEffect(() => {
        if (isOpen && inputRef.current) {
            inputRef.current.focus();
        }
    }, [isOpen]);

    useEffect(() => {
        const handleEscape = (e) => {
            if (e.key === 'Escape') onClose();
        };
        if (isOpen) {
            document.addEventListener('keydown', handleEscape);
            document.body.style.overflow = 'hidden';
        }
        return () => {
            document.removeEventListener('keydown', handleEscape);
            document.body.style.overflow = 'unset';
        };
    }, [isOpen, onClose]);

    const handleSubmit = (e) => {
        e.preventDefault();
        if (query.trim()) {
            onSearch(query.trim());
            onClose();
        }
    };

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 z-[100] flex items-start justify-center pt-20 md:pt-32">
            {/* Backdrop */}
            <div 
                className="absolute inset-0 bg-black/80 backdrop-blur-sm"
                onClick={onClose}
            />
            
            {/* Modal Content */}
            <div className="relative z-10 w-full max-w-2xl mx-4">
                <form onSubmit={handleSubmit}>
                    <div className="relative">
                        <input
                            ref={inputRef}
                            type="text"
                            value={query}
                            onChange={(e) => setQuery(e.target.value)}
                            placeholder="Search for products..."
                            className="w-full px-6 py-4 pl-14 bg-gray-900 border border-gray-700 rounded-2xl text-white text-lg placeholder-gray-500 focus:outline-none focus:border-orange-500 transition-colors"
                        />
                        <svg
                            className="absolute left-5 top-1/2 -translate-y-1/2 w-6 h-6 text-gray-500"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                        >
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                        </svg>
                        
                        {/* Close Button */}
                        <button
                            type="button"
                            onClick={onClose}
                            className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-500 hover:text-white transition-colors"
                        >
                            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                            </svg>
                        </button>
                    </div>
                    
                    {/* Quick Search Suggestions */}
                    <div className="mt-4 flex flex-wrap gap-2 justify-center">
                        {['shoes', 'sneakers', 'boots', 'sandals', 'face wash', 'skincare'].map((term) => (
                            <button
                                key={term}
                                type="button"
                                onClick={() => {
                                    onSearch(term);
                                    onClose();
                                }}
                                className="px-4 py-2 bg-gray-800 hover:bg-gray-700 text-gray-300 rounded-full text-sm transition-colors"
                            >
                                {term}
                            </button>
                        ))}
                    </div>
                    
                    {/* Search Button */}
                    <div className="mt-6 flex justify-center">
                        <button
                            type="submit"
                            disabled={loading || !query.trim()}
                            className="px-8 py-3 bg-orange-500 hover:bg-orange-600 rounded-full font-semibold transition-colors disabled:opacity-50 disabled:cursor-not-allowed text-white"
                        >
                            {loading ? 'Searching...' : 'Search'}
                        </button>
                    </div>
                </form>
                
                {/* Keyboard Shortcut Hint */}
                <p className="text-center text-gray-500 text-sm mt-4">
                    Press <kbd className="px-2 py-1 bg-gray-800 rounded text-xs">ESC</kbd> to close
                </p>
            </div>
        </div>
    );
};

export default SearchModal;
