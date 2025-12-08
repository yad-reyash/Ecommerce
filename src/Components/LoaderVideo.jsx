import { useEffect, useRef } from 'react'

/**
 * Autoplays a muted looping loader video on first load and reload.
 * Place the mp4 in `public/video/loader-video1.mp4` so it is served statically.
 */
export default function LoaderVideo() {
  const videoRef = useRef(null)

  useEffect(() => {
    const videoEl = videoRef.current
    if (!videoEl) return

    const attemptPlay = () => {
      // rewind on (re)load to ensure it starts from the beginning
      videoEl.currentTime = 0
      videoEl
        .play()
        .catch(err => {
          console.warn('Autoplay failed:', err)
        })
    }

    // Play immediately on mount
    attemptPlay()

    // Also play when the media reports it can play (covers reloads)
    videoEl.addEventListener('loadeddata', attemptPlay)
    return () => videoEl.removeEventListener('loadeddata', attemptPlay)
  }, [])

  return (
    <video
      ref={videoRef}
      src="/videos/egeon-concept-shoe-3d-animation-1080-publer.io.mp4"
      muted
      loop
      playsInline
      preload="auto"
      autoPlay
      style={{ width: '100%', height: 'auto', display: 'block' }}
    />
  )
}
