import { useEffect, useRef, useState } from 'react'

/**
 * Fullscreen intro video that autoplays on mount.
 * Closes after video ends or X seconds timeout.
 * Pass videoSrc, duration (ms), and onComplete callback.
 */
export default function FullscreenIntro({ videoSrc, duration = 100, onComplete }) {
  const videoRef = useRef(null)
  const [isVisible, setIsVisible] = useState(true)

  useEffect(() => {
    if (!isVisible) {
      onComplete?.()
      return
    }

    const videoEl = videoRef.current
    if (!videoEl) return

    // Auto-play
    videoEl.currentTime = 0
    videoEl.play().catch(err => console.warn('Autoplay failed:', err))

    // Close after duration timeout
    const timer = setTimeout(() => {
      setIsVisible(false)
    }, duration)

    // Close on video end
    const handleEnded = () => setIsVisible(false)
    videoEl.addEventListener('ended', handleEnded)

    return () => {
      clearTimeout(timer)
      videoEl.removeEventListener('ended', handleEnded)
    }
  }, [isVisible, duration, onComplete])

  if (!isVisible) return null

  return (
    <div className="fullscreen-intro">
      <video
        ref={videoRef}
        src={videoSrc}
        autoPlay
        muted
        loop={false}
        playsInline
        preload="auto"
        className="intro-video"
      />
    </div>
  )
}