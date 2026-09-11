/**
 * Kisan Web Project - Hero Video Background
 * Replaces the previous Three.js 3D Earth visualization.
 */

(function () {
  'use strict';

  const video = document.getElementById('hero-background-video');

  if (!video) return;

  // Ensure video starts automatically
  video.muted = true;
  video.loop = true;
  video.playsInline = true;

  // Try autoplay
  const playVideo = () => {
    const promise = video.play();

    if (promise !== undefined) {
      promise.catch(() => {
        console.log('Hero video autoplay was blocked by the browser.');
      });
    }
  };

  if (video.readyState >= 2) {
    playVideo();
  } else {
    video.addEventListener('loadeddata', playVideo, {
      once: true
    });
  }

  // Pause video when hero is not visible
  const hero = document.getElementById('hero');

  if ('IntersectionObserver' in window && hero) {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            playVideo();
          } else {
            video.pause();
          }
        });
      },
      {
        threshold: 0.1
      }
    );

    observer.observe(hero);
  }

})();