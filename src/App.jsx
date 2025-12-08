import { useState } from 'react'
import './App.css'
import FullscreenIntro from './Components/FullScreenVideoIntro.jsx'
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import NavBar from './Components/NavBar.jsx'
import Hero from './Components/Hero.jsx'
import ProductViewer from './Components/ProductViewer.jsx'
import Showcase from './Components/Showcase.jsx'
import Performance from './Components/Performance.jsx'
//import Features from './Components/Features.jsx'
//import Highlights from './Components/Highlights.jsx'
//import Footer from './Components/Footer.jsx'

gsap.registerPlugin(ScrollTrigger)
function App() {
  const [introComplete, setIntroComplete] = useState(false)

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
        <NavBar />
        <Hero />
        <ProductViewer />
        <Showcase />
        <Performance />
        {/* <Features />
        <Highlights />
        <Footer /> */}
      </main>
    </div>
  )
}

export default App