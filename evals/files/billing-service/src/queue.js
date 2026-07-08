// Minimal in-process job queue with retries.
// Jobs that exhaust retries land in deadLetters for manual review;
// nothing is reported back to the original caller.

const deadLetters = [];

async function enqueue(name, payload, handler, attempts = 3) {
  for (let i = 1; i <= attempts; i++) {
    try {
      return await handler(payload);
    } catch (err) {
      if (i === attempts) {
        deadLetters.push({ name, payload, error: err.message, failedAt: Date.now() });
        return null;
      }
      await new Promise((r) => setTimeout(r, 2 ** i * 100));
    }
  }
}

module.exports = { enqueue, deadLetters };
