const CACHE_NAME = 'hht-pwa-v1.2';
const STATIC_ASSETS = [
  '/',
  '/booking/create/',
  '/static/manifest.json',
  '/static/css/tokens.css',
  '/static/css/main.css',
  '/static/css/components.css',
  '/static/css/landing.css',
  '/static/css/booking.css',
  '/static/css/live-trip.css',
  '/static/css/driver.css',
  '/static/css/admin.css',
  '/static/js/graphics.js',
  '/static/js/app.js',
  '/static/js/map.js',
  '/static/js/booking.js',
  '/static/js/trip-simulator.js',
  '/static/js/driver.js',
  '/static/js/admin.js',
  'https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap',
  'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css',
  'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js'
];

// Install Event - Pre-cache App Shell
self.addEventListener('install', (event) => {
  self.skipWaiting();
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('[PWA Service Worker] Pre-caching App Shell');
      return cache.addAll(STATIC_ASSETS).catch(err => {
        console.warn('[PWA Service Worker] Asset caching warning:', err);
      });
    })
  );
});

// Activate Event - Clean Up Old Caches
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            console.log('[PWA Service Worker] Removing old cache', key);
            return caches.delete(key);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// Fetch Event - Network First with Cache Fallback
self.addEventListener('fetch', (event) => {
  // Only handle GET requests
  if (event.request.method !== 'GET') return;

  const url = new URL(event.request.url);

  // Ignore admin paths or non-http
  if (url.pathname.startsWith('/django-admin')) return;

  event.respondWith(
    fetch(event.request)
      .then((networkResponse) => {
        // Cache fresh response if valid
        if (networkResponse && networkResponse.status === 200 && networkResponse.type === 'basic') {
          const responseClone = networkResponse.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, responseClone);
          });
        }
        return networkResponse;
      })
      .catch(() => {
        // Fallback to cache when offline
        return caches.match(event.request).then((cachedResponse) => {
          if (cachedResponse) {
            return cachedResponse;
          }
          // Return offline page if html request
          if (event.request.headers.get('accept').includes('text/html')) {
            return caches.match('/');
          }
        });
      })
  );
});
