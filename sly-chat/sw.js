const CACHE_NAME = 'sly-chat-v8';

// Core assets — precached on install
const PRECACHE_ASSETS = [
    '/',
    '/index.html',
    '/manifest.json',
    '/icon-192.png',
    '/icon-512.png'
];

// CDN assets — cached on first use (stale-while-revalidate)
const CDN_HOSTS = [
    'fonts.googleapis.com',
    'fonts.gstatic.com',
    'cdn.jsdelivr.net',
    'ga.jspm.io',
    'www.gstatic.com'      // Draco decoder
];

// API endpoints — network only, never cache
const API_PATTERNS = [
    '/api/groq',
    '/api/gemini',
    '/api/tts',
    '/api/metrics'
];

self.addEventListener('install', e => {
    e.waitUntil(
        caches.open(CACHE_NAME).then(c => c.addAll(PRECACHE_ASSETS))
    );
    self.skipWaiting();
});

self.addEventListener('activate', e => {
    e.waitUntil(
        caches.keys().then(keys =>
            Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
        )
    );
    self.clients.claim();
});

self.addEventListener('fetch', e => {
    const url = new URL(e.request.url);

    // API calls → network only (never cache streaming/POST)
    if (API_PATTERNS.some(p => url.pathname.includes(p)) || e.request.method !== 'GET') {
        return; // Let browser handle normally
    }

    // CDN assets (fonts, Three.js, Draco) → stale-while-revalidate
    if (CDN_HOSTS.some(h => url.hostname === h)) {
        e.respondWith(
            caches.open(CACHE_NAME).then(async cache => {
                const cached = await cache.match(e.request);
                const fetchPromise = fetch(e.request).then(resp => {
                    if (resp.ok) cache.put(e.request, resp.clone());
                    return resp;
                }).catch(() => null);

                // Return cached immediately if available, otherwise wait for network
                return cached || fetchPromise || new Response('', { status: 503 });
            })
        );
        return;
    }

    // Local assets → network first, fallback cache
    e.respondWith(
        fetch(e.request).then(resp => {
            if (resp.ok) {
                const clone = resp.clone();
                caches.open(CACHE_NAME).then(c => c.put(e.request, clone));
            }
            return resp;
        }).catch(() => caches.match(e.request).then(r => r || caches.match('/index.html')))
    );
});
