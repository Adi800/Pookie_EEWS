const CACHE_NAME = 'earthquake-notification-cache-v2';
const urlsToCache = [
  '/',
  '/styles.css',
  '/script.js',
  '/manifest.json',
  'icon.png',
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => response || fetch(event.request))
  );
});
