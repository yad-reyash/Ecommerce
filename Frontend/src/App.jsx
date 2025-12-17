import { useState, useRef } from 'react'
import './App.css'
import FullscreenIntro from './Components/FullScreenVideoIntro.jsx'
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import NavBar from './Components/NavBar.jsx'
import Hero from './Components/Hero.jsx'
import ProductViewer from './Components/ProductViewer.jsx'
import Showcase from './Components/Showcase.jsx'
import Performance from './Components/Performance.jsx'
import ProductGrid from './Components/ProductGrid.jsx'
import SearchModal from './Components/SearchModal.jsx'
//import Features from './Components/Features.jsx'
//import Highlights from './Components/Highlights.jsx'
//import Footer from './Components/Footer.jsx'

gsap.registerPlugin(ScrollTrigger)
function App() {
  const [introComplete, setIntroComplete] = useState(false)
  const [isSearchOpen, setIsSearchOpen] = useState(false)
  const productGridRef = useRef(null)

  const handleSearch = (query) => {
    if (productGridRef.current) {
      productGridRef.current.performSearch(query);
      // Scroll to products section
      document.getElementById('products')?.scrollIntoView({ behavior: 'smooth' });
    }
  }

  return (
    <div className="app-root">
      {!introComplete && (
        <FullscreenIntro
          videoSrc="/videos/egeon-concept-shoe-3d-animation-1080-publer.io.mp4"
          duration={25000}
          onComplete={() => setIntroComplete(true)}
        />
      )}
      <main>
        <NavBar onSearchClick={() => setIsSearchOpen(true)} />
        <Hero />
        <ProductGrid ref={productGridRef} />
        <ProductViewer />
        <Showcase />
        <Performance />
        {/* <Features />
        <Highlights />
        <Footer /> */}
      </main>

      {/* Search Modal */}
      <SearchModal 
        isOpen={isSearchOpen}
        onClose={() => setIsSearchOpen(false)}
        onSearch={handleSearch}
      />
    </div>
  )
}

export default App