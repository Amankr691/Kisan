/**
 * Kisan Web Project - Real-Time Geolocation & 7-Day Weather Forecaster
 * Integrates browser geolocation, Open-Meteo REST service, and 7-day agricultural forecasts.
 */

(function () {
  'use strict';

  // Global state for detected climate
  window.userLocation = {
    lat: 28.6139,
    lon: 77.2090,
    locationName: 'Indo-Gangetic Basin (Default)',
    temperature: 26.5,
    rainfall: 45.0,
    humidity: 62.0,
  };

  const weatherIcons = {
    sun: `<svg class="w-8 h-8 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"/></svg>`,
    'cloud-sun': `<svg class="w-8 h-8 text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z"/></svg>`,
    cloud: `<svg class="w-8 h-8 text-slate-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z"/></svg>`,
    'cloud-rain': `<svg class="w-8 h-8 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 13v5m-4-3v5m-4-1v5m1-16a4 4 0 00-4 4 4 4 0 001.172 2.828A5 5 0 1016 13h1a4 4 0 004-4 4 4 0 00-4-4"/></svg>`,
    'cloud-rain-heavy': `<svg class="w-8 h-8 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 14v4m4-3v4m4-1v4M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z"/></svg>`,
    'cloud-drizzle': `<svg class="w-8 h-8 text-teal-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v3m4-2v3m-8-1v3M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z"/></svg>`,
    'cloud-lightning': `<svg class="w-8 h-8 text-amber-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>`,
  };

  async function fetchWeatherData(lat, lon, locationName) {
    try {
      const res = await fetch(`/api/weather/current?lat=${lat}&lon=${lon}&location=${encodeURIComponent(locationName)}`);
      const json = await res.json();
      const data = json.data;

      window.userLocation = {
        lat: lat,
        lon: lon,
        locationName: data.location_name || locationName,
        temperature: data.temperature,
        rainfall: data.rainfall_probability,
        humidity: data.humidity,
      };

      updateWeatherUI(data);
    } catch (err) {
      console.warn('Weather fetch error, using local fallback:', err);
    }
  }

  function updateWeatherUI(data) {
    // 1. Update Header Live Badge
    const navTemp = document.getElementById('nav-weather-temp');
    const navCond = document.getElementById('nav-weather-cond');
    const navLoc = document.getElementById('nav-weather-loc');

    if (navTemp) navTemp.textContent = `${Math.round(data.temperature)}°C`;
    if (navCond) navCond.textContent = data.weather_condition;
    if (navLoc) navLoc.textContent = data.location_name;

    // 2. Update Main Weather Section Today Card
    const currentTemp = document.getElementById('weather-current-temp');
    const currentCond = document.getElementById('weather-current-cond');
    const currentLoc = document.getElementById('weather-current-location');
    const currentHumidity = document.getElementById('weather-current-humidity');
    const currentRain = document.getElementById('weather-current-rain');
    const currentWind = document.getElementById('weather-current-wind');
    const currentIcon = document.getElementById('weather-current-icon');
    const currentAdvisory = document.getElementById('weather-current-advisory');

    if (currentTemp) currentTemp.textContent = `${Math.round(data.temperature)}°C`;
    if (currentCond) currentCond.textContent = data.weather_condition;
    if (currentLoc) currentLoc.textContent = data.location_name;
    if (currentHumidity) currentHumidity.textContent = `${Math.round(data.humidity)}%`;
    if (currentRain) currentRain.textContent = `${Math.round(data.rainfall_probability)}%`;
    if (currentWind) currentWind.textContent = `${data.wind_speed_kmh} km/h`;

    const iconKey = data.forecast && data.forecast[0] ? data.forecast[0].icon : 'sun';
    if (currentIcon) {
      currentIcon.innerHTML = weatherIcons[iconKey] || weatherIcons.sun;
    }

    if (currentAdvisory && data.forecast && data.forecast[0]) {
      currentAdvisory.textContent = data.forecast[0].advisory;
    }

    // 3. Render 7-Day Forecast Strip
    const forecastGrid = document.getElementById('weather-forecast-grid');
    if (forecastGrid && data.forecast) {
      forecastGrid.innerHTML = '';
      data.forecast.forEach((day, index) => {
        const isToday = index === 0;
        const iconSvg = weatherIcons[day.icon] || weatherIcons.sun;
        const dayCard = document.createElement('div');
        dayCard.className = `glass-card tilt-card p-4 rounded-xl flex flex-col items-center justify-between text-center transition-all ${
          isToday ? 'border-emerald-500/40 bg-emerald-950/20' : ''
        }`;

        dayCard.innerHTML = `
          <div class="tilt-glare"></div>
          <div class="tilt-content w-full flex flex-col items-center">
            <span class="text-xs font-semibold uppercase tracking-wider ${isToday ? 'text-emerald-400 font-bold' : 'text-slate-400'}">
              ${isToday ? 'Today' : day.day}
            </span>
            <span class="text-[10px] text-slate-500 mb-2">${day.date.slice(5)}</span>
            <div class="my-2 transform hover:scale-110 transition-transform">
              ${iconSvg}
            </div>
            <span class="text-xs font-medium text-slate-200 mt-1 line-clamp-1">${day.condition}</span>
            <div class="flex items-center gap-2 mt-2">
              <span class="text-sm font-bold text-white">${Math.round(day.max_temp)}°</span>
              <span class="text-xs text-slate-400">${Math.round(day.min_temp)}°</span>
            </div>
            <!-- Rain likelihood meter -->
            <div class="w-full bg-slate-800/80 rounded-full h-1.5 mt-3 overflow-hidden" title="Rain probability: ${day.rain_prob}%">
              <div class="bg-cyan-400 h-full rounded-full transition-all" style="width: ${Math.min(100, Math.max(5, day.rain_prob))}%"></div>
            </div>
            <span class="text-[10px] text-cyan-300 mt-1">💧 ${day.rain_prob}% Rain</span>
          </div>
        `;
        forecastGrid.appendChild(dayCard);
      });

      if (window.init3DTilt) window.init3DTilt();
    }
  }

  function detectUserLocation() {
    const locStatus = document.getElementById('location-detect-status');
    if (locStatus) locStatus.textContent = 'Acquiring GPS coordinates...';

    if ('geolocation' in navigator) {
      navigator.geolocation.getCurrentPosition(
        async (position) => {
          const lat = position.coords.latitude;
          const lon = position.coords.longitude;
          if (locStatus) locStatus.textContent = 'Detected! Fetching satellite weather...';

          let locationName = 'Local Farmland';
          try {
            // Reverse geocode via free bigdatacloud or osm
            const geoResp = await fetch(`https://api.bigdatacloud.net/data/reverse-geocode-client?latitude=${lat}&longitude=${lon}&localityLanguage=en`);
            if (geoResp.ok) {
              const geoData = await geoResp.json();
              locationName = `${geoData.city || geoData.locality || geoData.principalSubdivision}, ${geoData.countryName || 'India'}`;
            }
          } catch (e) {
            locationName = `${lat.toFixed(2)}°N, ${lon.toFixed(2)}°E`;
          }

          if (locStatus) locStatus.textContent = `Active: ${locationName}`;
          fetchWeatherData(lat, lon, locationName);
        },
        (error) => {
          console.log('Geolocation denied or unavailable, falling back to IP/default:', error.message);
          if (locStatus) locStatus.textContent = 'Regional Farm (Auto IP)';
          fetchIPLocation();
        },
        { timeout: 8000 }
      );
    } else {
      fetchIPLocation();
    }
  }

  async function fetchIPLocation() {
    try {
      const res = await fetch('https://ipapi.co/json/');
      if (res.ok) {
        const ipData = await res.json();
        const lat = ipData.latitude || 28.6139;
        const lon = ipData.longitude || 77.2090;
        const locName = `${ipData.city || 'Regional'}, ${ipData.region || 'Punjab'}`;
        fetchWeatherData(lat, lon, locName);
        return;
      }
    } catch (e) {
      // Fallback
    }
    fetchWeatherData(28.6139, 77.2090, 'Indo-Gangetic Basin');
  }

  // Expose globally
  window.detectUserLocation = detectUserLocation;
  window.fetchWeatherData = fetchWeatherData;

  document.addEventListener('DOMContentLoaded', () => {
    detectUserLocation();

    const refreshBtn = document.getElementById('btn-refresh-weather');
    if (refreshBtn) {
      refreshBtn.addEventListener('click', () => {
        detectUserLocation();
      });
    }
  });
})();
