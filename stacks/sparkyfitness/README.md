# SparkyFitness

## Required values

| Variable | Value | Generate |
| --- | --- | --- |
| `DATABASE_PASSWORD` | Strong PostgreSQL password | `openssl rand -base64 32` |
| `SPARKY_FITNESS_APP_DB_PASSWORD` | Strong application-database password | `openssl rand -base64 32` |
| `SPARKY_FITNESS_FRONTEND_URL` | `https://health.zech.co` | — |
| `SPARKY_FITNESS_API_ENCRYPTION_KEY` | Generated 64-character hexadecimal key | `openssl rand -hex 32` |
| `BETTER_AUTH_SECRET` | Generated persistent secret | `openssl rand -hex 32` |
| `SPARKY_FITNESS_EMAIL_HOST` | SMTP host | External |
| `SPARKY_FITNESS_EMAIL_USER` | SMTP username | External |
| `SPARKY_FITNESS_EMAIL_PASS` | SMTP password | External |
| `SPARKY_FITNESS_OIDC_CLIENT_ID` | Authentik client ID | Authentik |
| `SPARKY_FITNESS_OIDC_CLIENT_SECRET` | Authentik client secret | Authentik |

## Update `.env`

To update the local `.env` with the generated values:

```bash
sed -i "s|^DATABASE_PASSWORD=.*|DATABASE_PASSWORD=$(openssl rand -base64 32)|" .env
sed -i "s|^SPARKY_FITNESS_APP_DB_PASSWORD=.*|SPARKY_FITNESS_APP_DB_PASSWORD=$(openssl rand -base64 32)|" .env
sed -i "s|^SPARKY_FITNESS_API_ENCRYPTION_KEY=.*|SPARKY_FITNESS_API_ENCRYPTION_KEY=$(openssl rand -hex 32)|" .env
sed -i "s|^BETTER_AUTH_SECRET=.*|BETTER_AUTH_SECRET=$(openssl rand -hex 32)|" .env
```

## Authentik OIDC

| Authentik setting | Value |
| --- | --- |
| Provider/application | SparkyFitness |
| Redirect URI (Strict Authorization) | `https://health.zech.co/api/auth/sso/callback/authentik` |
