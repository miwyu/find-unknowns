// Thin wrapper around the payment provider's API.
// chargeId is the provider-side id from the original charge.

async function refundCharge(chargeId, amountCents) {
  // Real implementation calls the provider over HTTPS. Simulated here.
  if (amountCents <= 0) throw new Error('invalid_amount');
  return { providerRefundId: `re_${chargeId}_${amountCents}`, status: 'succeeded' };
}

module.exports = { refundCharge };
