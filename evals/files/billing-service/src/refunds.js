const { refundCharge } = require('./gateway');
const { enqueue } = require('./queue');
const ledger = require('./ledger');

// POST /refunds handler. Since the ledger change, this no longer waits for
// the provider: it records intent and settles in the background.
async function requestRefund({ chargeId, amountCents, requestId }) {
  const idempotencyKey = `refund:${chargeId}:${requestId}`;

  const { entry, duplicate } = ledger.record(idempotencyKey, {
    chargeId,
    amountCents,
  });
  if (duplicate) {
    return { status: entry.state, chargeId, amountCents: entry.amountCents };
  }

  // Fire and forget: provider call happens in the queue with retries.
  enqueue('refund', { chargeId, amountCents }, async (job) => {
    const result = await refundCharge(job.chargeId, job.amountCents);
    ledger.settle(idempotencyKey, result.providerRefundId);
    return result;
  });

  return { status: 'pending', chargeId, amountCents };
}

module.exports = { requestRefund };
