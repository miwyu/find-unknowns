const express = require('express');
const { requestRefund } = require('./refunds');

const app = express();
app.use(express.json());

app.post('/refunds', async (req, res) => {
  try {
    const result = await requestRefund({
      chargeId: req.body.chargeId,
      amountCents: req.body.amountCents,
      requestId: req.get('X-Request-Id') || `${Date.now()}`,
    });
    res.status(202).json(result);
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

app.listen(process.env.PORT || 4000);
