# Implementation plan: per-client request metrics (agreed 2026-07-06)

Goal: partners keep asking support "how many API calls did we make this month?"
Expose our own numbers so they stop guessing from their logs.

## Steps

1. **Add a `src/metrics.js` module** that records one counter per
   `(clientId, route, day)` using the existing StatsD client in
   `src/statsd.js`. Keep the metric name format `api.calls.<clientId>.<route>`.

2. **Record counts in the existing request-logging middleware**
   `src/middleware/requestLog.js` — add one `metrics.increment(...)` call
   right after the existing log line, so counting stays out of route handlers.

3. **Expose `GET /v2/metrics`** returning the caller's own counts for the
   current month, JSON shape `{ clientId, month, counts: { <route>: n } }`.
   Restrict it to **admin-tier API keys only** — regular partner keys should
   get a 403.

4. Tests for: counts increment on authenticated requests, metrics endpoint
   shape, and the 403 for non-admin keys.

Out of scope: dashboards, historical backfill, webhook traffic counting.
