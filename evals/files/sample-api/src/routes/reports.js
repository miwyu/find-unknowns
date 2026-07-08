const { Router } = require('express');
const redis = require('../redis');

const router = Router();

// Report generation is CPU-heavy; results are cached in Redis for 5 minutes.
router.get('/:reportId', async (req, res) => {
  const cacheKey = `report:${req.client.clientId}:${req.params.reportId}`;
  const cached = await redis.get(cacheKey).catch(() => null);
  if (cached) return res.json(JSON.parse(cached));

  const report = { id: req.params.reportId, rows: [], generatedAt: new Date().toISOString() };
  await redis.set(cacheKey, JSON.stringify(report), 'EX', 300).catch(() => {});
  res.json(report);
});

module.exports = router;
