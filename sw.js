// Service Worker for PWA - 缓存所有文件实现离线访问
const CACHE_NAME = 'homework-workbench-v3';
const FILES_TO_CACHE = [
  '.',
  'index.html',
  'manifest.json',
  'icon-192.png',
  'icon-512.png'
];

// 安装：预缓存所有核心文件
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(FILES_TO_CACHE);
    })
  );
  self.skipWaiting();
});

// 激活：清理旧缓存
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((names) => {
      return Promise.all(
        names.filter((name) => name !== CACHE_NAME).map((name) => caches.delete(name))
      );
    })
  );
  self.clients.claim();
});

// 请求拦截：HTML用网络优先，其他资源用缓存优先
self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);
  // HTML页面：网络优先，确保始终获取最新版本（密钥等JS逻辑在HTML中）
  if (event.request.destination === 'document' || url.pathname.endsWith('.html') || url.pathname === '/' || url.pathname.endsWith('/')) {
    event.respondWith(
      fetch(event.request).then((response) => {
        if (response && response.status === 200) {
          const clone = response.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone));
        }
        return response;
      }).catch(() => {
        return caches.match(event.request);
      })
    );
  } else {
    // 其他资源（图片、manifest等）：缓存优先，后台更新
    event.respondWith(
      caches.match(event.request).then((cached) => {
        const fetchPromise = fetch(event.request).then((response) => {
          if (response && response.status === 200) {
            const clone = response.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone));
          }
          return response;
        }).catch(() => cached);
        return cached || fetchPromise;
      })
    );
  }
});
