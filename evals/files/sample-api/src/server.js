const express = require('express');
const pino = require('pino');
const { apiKeyAuth } = require('./middleware/auth');
const usersRouter = require('./routes/users');
const reportsRouter = require('./routes/reports');
const webhooksRouter = require('./routes/webhooks');

const log = pino();
const app = express();

app.use(express.json({ limit: '1mb' }));

// Webhooks are unauthenticated by design (verified via HMAC signature instead).
app.use('/webhooks', webhooksRouter);

// Everything below requires a partner API key.
app.use(apiKeyAuth);
app.use('/v2/users', usersRouter);
app.use('/v2/reports', reportsRouter);

const port = process.env.PORT || 3000;
app.listen(port, () => log.info({ port }, 'acme-partner-api listening'));
