// Append-only refund ledger, introduced with the async-refund change.
// The idempotency key makes retries and double-submits safe: a second
// entry with the same key is ignored and the original entry returned.

const entries = new Map(); // idempotencyKey -> entry

function record(idempotencyKey, entry) {
  const existing = entries.get(idempotencyKey);
  if (existing) return { entry: existing, duplicate: true };
  const stored = { ...entry, recordedAt: Date.now(), state: 'pending' };
  entries.set(idempotencyKey, stored);
  return { entry: stored, duplicate: false };
}

function settle(idempotencyKey, providerRefundId) {
  const entry = entries.get(idempotencyKey);
  if (entry) {
    entry.state = 'settled';
    entry.providerRefundId = providerRefundId;
  }
}

module.exports = { record, settle };
