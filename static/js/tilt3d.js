/**
 * Kisan Web Project - 3D Perspective Tilt Engine
 * Provides interactive mouse-tracking 3D tilt and specular lighting effects
 * for floating glassmorphic cards.
 */

(function () {
  'use strict';

  function attachTiltToElement(card) {
    if (card._tiltAttached) return;
    card._tiltAttached = true;

    // Ensure glare overlay element exists
    let glare = card.querySelector('.tilt-glare');
    if (!glare) {
      glare = document.createElement('div');
      glare.className = 'tilt-glare';
      card.appendChild(glare);
    }

    const maxTilt = 12; // Maximum tilt degrees

    function onMouseMove(e) {
      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;

      const centerX = rect.width / 2;
      const centerY = rect.height / 2;

      const rotateX = ((centerY - y) / centerY) * maxTilt;
      const rotateY = ((x - centerX) / centerX) * maxTilt;

      card.style.transform = `perspective(1000px) rotateX(${rotateX.toFixed(2)}deg) rotateY(${rotateY.toFixed(2)}deg) scale3d(1.02, 1.02, 1.02)`;

      // Move specular glare position
      const glareX = (x / rect.width) * 100;
      const glareY = (y / rect.height) * 100;
      glare.style.background = `radial-gradient(circle at ${glareX}% ${glareY}%, rgba(255, 255, 255, 0.22), transparent 60%)`;
      glare.style.opacity = '1';
    }

    function onMouseLeave() {
      card.style.transition = 'transform 0.5s cubic-bezier(0.2, 0.8, 0.2, 1)';
      card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)';
      glare.style.opacity = '0';

      setTimeout(() => {
        card.style.transition = '';
      }, 500);
    }

    function onMouseEnter() {
      card.style.transition = 'transform 0.1s ease-out';
    }

    card.addEventListener('mousemove', onMouseMove);
    card.addEventListener('mouseleave', onMouseLeave);
    card.addEventListener('mouseenter', onMouseEnter);
  }

  function init3DTilt() {
    const cards = document.querySelectorAll('.tilt-card');
    cards.forEach((card) => attachTiltToElement(card));
  }

  // Export globally
  window.init3DTilt = init3DTilt;

  document.addEventListener('DOMContentLoaded', () => {
    init3DTilt();
  });
})();
