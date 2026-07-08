const { Router } = require('express');

const router = Router();

// Cheap reads — partners poll this heavily.
router.get('/:id', (req, res) => {
  res.json({ id: req.params.id, client: req.client.clientId, name: 'Sample User' });
});

// Writes are much more expensive than reads (fan out to billing + audit log).
router.post('/', (req, res) => {
  res.status(201).json({ id: 'u_new', ...req.body });
});

module.exports = router;
