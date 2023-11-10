const CACHE_NAME = "version-1",
  urlsToCache = ["/static/main.js"],
  self = this;
"serviceWorker" in navigator &&
  window.addEventListener("load", () => {
    navigator.serviceWorker
      .register("/static/sw.js")
      .then((e) => console.log("Success: ", e.scope))
      .catch((e) => console.log("Failure: ", e));
  });
self.addEventListener("install", (e) => {
  e.waitUntil(
    caches
      .open(CACHE_NAME)
      .then((e) => (console.log("Opened cache"), e.addAll(urlsToCache)))
  );
});
self.addEventListener("fetch", (e) => {
  let { pathname: t } = new URL(e.request.url);
  t.startsWith("/api/") ||
    e.respondWith(
      (async () => {
        const t = await caches.match(e.request);
        return t ? (e.waitUntil(cache.add(e.request)), t) : fetch(e.request);
      })()
    );
});
self.addEventListener("activate", (e) => {
  const t = [];
  t.push(CACHE_NAME);
  e.waitUntil(
    caches.keys().then((e) =>
      Promise.all(
        e.map((e) => {
          if (!t.includes(e)) return caches.delete(e);
        })
      )
    )
  );
});
