import { useEffect, useRef } from "react";

const Hero = () => {
  const videoRef = useRef(null);

  useEffect(() => {
    const vid = videoRef.current;
    if (vid) {
      vid.muted = true;
      vid.loop = true;
      vid.playbackRate = 2;     // Play at double speed
      vid.playsInline = true;

      // Try to play — some browsers may require a user gesture for autoplay/video
      const playPromise = vid.play();
      if (playPromise !== undefined) {
        playPromise.catch(error => {
          console.warn("Video autoplay failed:", error);
        });
      }
    }
  }, []);

  return (
    <section id="hero">
     
      <video
        ref={videoRef}
        src="/videos/hero.mp4"
        style={{ width: "75%", height: "auto" }}
      />
    </section>
  );
};

export default Hero;
