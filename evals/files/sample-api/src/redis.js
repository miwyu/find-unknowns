const Redis = require('ioredis');

// Shared client, currently used only for response caching in routes/reports.js.
// The instance is a single managed node (no cluster mode).
const redis = new Redis(process.env.REDIS_URL || 'redis://localhost:6379', {
  maxRetriesPerRequest: 2,
  enableOfflineQueue: false,
});

module.exports = redis;
