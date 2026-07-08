# acme-partner-api

Partner-facing REST API for Acme. Serves third-party integrators.

Every partner authenticates with an API key (`X-Api-Key` header). Keys map to a
client id and a plan tier (`free`, `pro`, `enterprise`) — see
`src/middleware/auth.js`.

Redis is used for response caching (`src/redis.js`). Run `npm start` after
setting `REDIS_URL`.

Note: `/webhooks/github` is called by GitHub, not by partners — it is
unauthenticated by design and can burst heavily during busy release windows.
