/**
 * Kisan Web Project - 3D Animated Showcase Carousel
 * Provides dynamic 3D cylinder perspective rotation for visual cards and video demos.
 */

(function () {
  'use strict';

  const carouselItemsData = [
    {
      title: 'Precision Agri-Drone Foliar Spray',
      category: 'Smart Automation',
      desc: '10L payload electrostatic spraying covering 1 acre in 7 minutes with 90% water reduction.',
      badge: '50% Subsidy',
      badgeColor: 'emerald',
      image: 'https://images.unsplash.com/photo-1508614589041-895b88991e3e?auto=format&fit=crop&w=800&q=80',
      videoUrl: 'https://www.youtube.com/embed/ScMzIvxBSi4?autoplay=1'
    },
    {
      title: 'Wetland Crawler Mini-Combine',
      category: 'Harvesting Machinery',
      desc: 'Rubber-track technology that operates seamlessly in flooded paddy fields without sinking.',
      badge: 'High Efficiency',
      badgeColor: 'amber',
      image: 'https://images.unsplash.com/photo-1595246140625-573b715d11dc?auto=format&fit=crop&w=800&q=80',
      videoUrl: 'https://www.youtube.com/embed/fJ9rUzIMcZQ?autoplay=1'
    },
    {
      title: 'IoT Solar Drip Fertigation',
      category: 'Precision Irrigation',
      desc: 'Autonomous cellular soil moisture telemetry and automated solenoid fertigation valves.',
      badge: '55% Subsidy',
      badgeColor: 'cyan',
      image: 'https://images.unsplash.com/photo-1563245372-f21724e3856d?auto=format&fit=crop&w=800&q=80',
      videoUrl: 'https://www.youtube.com/embed/kJQP7kiw5Fk?autoplay=1'
    },
    {
      title: 'GPS Laser Land Leveling',
      category: 'Resource Conservation',
      desc: 'Dual-axis rotating laser scraper leveling soil to ±2mm tolerance, saving 25% irrigation water.',
      badge: 'Water Saver',
      badgeColor: 'emerald',
      image: 'https://images.unsplash.com/photo-1589923188900-85dae523342b?auto=format&fit=crop&w=800&q=80',
      videoUrl: 'https://www.youtube.com/embed/J---aiyznGQ?autoplay=1'
    },
    {
      title: 'High-Density Silver Mulch Farming',
      category: 'Vegetable Production',
      desc: 'Integrated raised-bed drip and reflective mulch yielding up to 350 quintals/acre of hybrid tomatoes.',
      badge: 'Bumper Yield',
      badgeColor: 'amber',
      image: 'https://images.unsplash.com/photo-1592841200221-a6898f307baa?auto=format&fit=crop&w=800&q=80',
      videoUrl: 'https://www.youtube.com/embed/b1hPjLhNlZc?autoplay=1'
    }
  ];

  let currentIndex = 0;
  let autoPlayTimer = null;

  function renderCarousel() {
    const ring = document.getElementById('carousel-3d-ring');
    const dotsContainer = document.getElementById('carousel-dots');
    if (!ring) return;

    ring.innerHTML = '';
    if (dotsContainer) dotsContainer.innerHTML = '';

    const total = carouselItemsData.length;
    const angleStep = 360 / total;
    // Calculate radius based on container width
    const containerWidth = ring.parentElement.clientWidth;
    const radius = Math.min(420, Math.max(260, containerWidth * 0.38));

    carouselItemsData.forEach((item, index) => {
      const cardAngle = angleStep * index;
      const card = document.createElement('div');
      card.className = 'carousel-3d-item glass-card rounded-2xl p-4 flex flex-col justify-between cursor-pointer border border-emerald-500/20';
      card.style.width = '320px';
      card.style.height = '380px';
      card.style.transform = `rotateY(${cardAngle}deg) translateZ(${radius}px)`;

      card.innerHTML = `
        <div class="relative w-full h-44 rounded-xl overflow-hidden mb-3 group">
          <img src="${item.image}" alt="${item.title}" class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110" />
          <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent"></div>
          <span class="absolute top-2 right-2 px-2.5 py-1 text-xs font-semibold rounded-full badge-glow-${item.badgeColor}">
            ${item.badge}
          </span>
          <button onclick="window.openVideoModal('${item.title}', '${item.videoUrl}')" class="absolute inset-0 m-auto w-12 h-12 rounded-full bg-emerald-500/80 hover:bg-emerald-400 text-white flex items-center justify-center backdrop-blur shadow-lg transition-transform hover:scale-110">
            <svg class="w-5 h-5 ml-0.5" fill="currentColor" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
          </button>
        </div>
        <div class="flex-1 flex flex-col justify-between">
          <div>
            <span class="text-xs uppercase tracking-wider font-semibold text-emerald-400">${item.category}</span>
            <h4 class="text-base font-bold text-white mt-1 line-clamp-1">${item.title}</h4>
            <p class="text-xs text-slate-300 mt-1 line-clamp-2">${item.desc}</p>
          </div>
          <div class="pt-3 border-t border-white/10 flex items-center justify-between text-xs">
            <button onclick="window.openVideoModal('${item.title}', '${item.videoUrl}')" class="text-emerald-400 hover:text-emerald-300 font-semibold flex items-center gap-1">
              Watch Field Demo
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
            </button>
            <span class="text-slate-400">3D Interactive</span>
          </div>
        </div>
      `;

      card.addEventListener('click', (e) => {
        if (!e.target.closest('button')) {
          rotateTo(index);
        }
      });

      ring.appendChild(card);

      // Create indicator dot
      if (dotsContainer) {
        const dot = document.createElement('button');
        dot.className = `w-2.5 h-2.5 rounded-full transition-all duration-300 ${index === 0 ? 'bg-emerald-400 w-6' : 'bg-white/30 hover:bg-white/60'}`;
        dot.addEventListener('click', () => rotateTo(index));
        dotsContainer.appendChild(dot);
      }
    });

    updateCarouselTransform();
  }

  function updateCarouselTransform() {
    const ring = document.getElementById('carousel-3d-ring');
    const dotsContainer = document.getElementById('carousel-dots');
    if (!ring) return;

    const total = carouselItemsData.length;
    const angleStep = 360 / total;
    const currentAngle = -currentIndex * angleStep;

    ring.style.transform = `rotateY(${currentAngle}deg)`;

    // Update items active state
    const items = ring.querySelectorAll('.carousel-3d-item');
    items.forEach((item, idx) => {
      if (idx === currentIndex) {
        item.style.opacity = '1';
        item.style.filter = 'brightness(1.05)';
      } else {
        item.style.opacity = '0.55';
        item.style.filter = 'brightness(0.75)';
      }
    });

    // Update indicator dots
    if (dotsContainer) {
      const dots = dotsContainer.children;
      for (let d = 0; d < dots.length; d++) {
        if (d === currentIndex) {
          dots[d].className = 'w-6 h-2.5 rounded-full bg-emerald-400 transition-all duration-300';
        } else {
          dots[d].className = 'w-2.5 h-2.5 rounded-full bg-white/30 hover:bg-white/60 transition-all duration-300';
        }
      }
    }
  }

  function rotateTo(index) {
    const total = carouselItemsData.length;
    currentIndex = ((index % total) + total) % total;
    updateCarouselTransform();
  }

  function nextSlide() {
    rotateTo(currentIndex + 1);
  }

  function prevSlide() {
    rotateTo(currentIndex - 1);
  }

  function startAutoPlay() {
    stopAutoPlay();
    autoPlayTimer = setInterval(nextSlide, 4500);
  }

  function stopAutoPlay() {
    if (autoPlayTimer) clearInterval(autoPlayTimer);
  }

  // Global Video Modal Handler
  window.openVideoModal = function (title, videoUrl) {
    const modal = document.getElementById('video-modal');
    const iframe = document.getElementById('video-modal-iframe');
    const titleEl = document.getElementById('video-modal-title');
    if (!modal || !iframe) return;

    if (titleEl) titleEl.textContent = title;
    iframe.src = videoUrl;
    modal.classList.remove('hidden');
    modal.classList.add('flex');
  };

  window.closeVideoModal = function () {
    const modal = document.getElementById('video-modal');
    const iframe = document.getElementById('video-modal-iframe');
    if (!modal || !iframe) return;

    iframe.src = '';
    modal.classList.add('hidden');
    modal.classList.remove('flex');
  };

  document.addEventListener('DOMContentLoaded', () => {
    renderCarousel();
    startAutoPlay();

    const nextBtn = document.getElementById('carousel-next-btn');
    const prevBtn = document.getElementById('carousel-prev-btn');
    const scene = document.querySelector('.carousel-3d-scene');

    if (nextBtn) nextBtn.addEventListener('click', () => { nextSlide(); startAutoPlay(); });
    if (prevBtn) prevBtn.addEventListener('click', () => { prevSlide(); startAutoPlay(); });

    if (scene) {
      scene.addEventListener('mouseenter', stopAutoPlay);
      scene.addEventListener('mouseleave', startAutoPlay);
    }

    window.addEventListener('resize', () => {
      renderCarousel();
    });
  });
})();
