const crypto = require('crypto');

// In production this table lives in Postgres and is cached in-process for 60s.
// Plan tiers matter commercially: enterprise partners are contractually
// promised "no throttling below 1000 req/min".
const KEYS = new Map([
  ['ak_live_9f2c', { clientId: 'globex', tier: 'enterprise' }],
  ['ak_live_77aa', { clientId: 'initech', tier: 'pro' }],
  ['ak_live_c01d', { clientId: 'hooli', tier: 'free' }],
]);

function apiKeyAuth(req, res, next) {
  const key = req.get('X-Api-Key');
  if (!key || !KEYS.has(key)) {
    return res.status(401).json({ error: 'invalid_api_key' });
  }
  req.client = KEYS.get(key);
  next();
}

function verifyWebhookSignature(payload, signature, secret) {
  const expected = crypto.createHmac('sha256', secret).update(payload).digest('hex');
  return crypto.timingSafeEqual(Buffer.from(signature), Buffer.from(expected));
}

module.exports = { apiKeyAuth, verifyWebhookSignature };
