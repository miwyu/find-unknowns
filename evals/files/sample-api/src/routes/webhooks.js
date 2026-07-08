const { Router } = require('express');
const { verifyWebhookSignature } = require('../middleware/auth');

const router = Router();

// Called by GitHub, not by partners. Unauthenticated (HMAC-verified instead).
// Bursts hard during release windows — hundreds of deliveries in a few seconds.
// GitHub retries failed deliveries with backoff, but disables the hook after
// repeated failures, so rejecting these has real consequences.
router.post('/github', (req, res) => {
  const sig = req.get('X-Hub-Signature-256') || '';
  const ok = verifyWebhookSignature(
    JSON.stringify(req.body),
    sig.replace('sha256=', ''),
    process.env.GITHUB_WEBHOOK_SECRET || 'dev-secret'
  );
  if (!ok) return res.status(401).json({ error: 'bad_signature' });
  res.status(202).json({ received: true });
});

module.exports = router;
