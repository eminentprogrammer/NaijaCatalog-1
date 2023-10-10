// Install and activate the service worker
self.addEventListener('install', (event) => {
     event.waitUntil(
       caches.open('app-cache').then((cache) => {
         return cache.addAll([
           '/',
           '/homepage.html',
           '/static/css/styles.css',
           '/static/js/custom.js',
           '/static/images/naijacatalog.png',
         ]);
       })
     );
  });
   
   self.addEventListener('activate', (event) => {
     event.waitUntil(
       caches.keys().then((cacheNames) => {
         return Promise.all(
           cacheNames.filter((cacheName) => {
            return cacheName.startsWith('app-cache') && cacheName !== 'app-cache';
            }).map((cacheName) => {
            return caches.delete(cacheName);
          })
        );
      })
    );
  });
  
  // Fetch resources from cache or network
  self.addEventListener('fetch', (event) => {
     event.respondWith(
       caches.match(event.request).then((response) => {
         return response || fetch(event.request);
       })
     );
  });