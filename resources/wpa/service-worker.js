const CACHE_NAME = 'v0k1nt-anime-cache-v1';
const urlsToCache = ['/', '/search', '/release', '/static/css/index.css', '/static/js/index.js', '/static/js/search.js'];

self.addEventListener('install', (event) => {
	event.waitUntil(
		caches.open(CACHE_NAME).then((cache) => {
			return cache.addAll(urlsToCache);
		})
	);
});

self.addEventListener('fetch', (event) => {
	event.respondWith(
		caches.match(event.request).then((response) => {
			return response || fetch(event.request);
		})
	);
});
