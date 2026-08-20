# Paperless-ngx

## Required values

| Variable | Value | Generate |
| --- | --- | --- |
| `DATABASE_PASSWORD` | Strong PostgreSQL password | `openssl rand -base64 32` |
| `PAPERLESS_SECRET_KEY` | Generated persistent secret | `openssl rand -base64 64` |
| `PAPERLESS_SOCIALACCOUNT_PROVIDERS` | Replace `<client_id>` with the Authentik client ID | Authentik |
| `PAPERLESS_SOCIALACCOUNT_PROVIDERS` | Replace `<secret>` with the Authentik client secret | Authentik |

## Update `.env`

To update the local `.env` with the generated values:

```bash
sed -i "s|^DATABASE_PASSWORD=.*|DATABASE_PASSWORD=$(openssl rand -base64 32)|" .env
sed -i "s|^PAPERLESS_SECRET_KEY=.*|PAPERLESS_SECRET_KEY=$(openssl rand -base64 64)|" .env
```

## Authentik OIDC

| Authentik setting | Value |
| --- | --- |
| Provider/application | Paperless-ngx |
| Redirect URI (Strict Authorization) | `https://paperless.zech.co/accounts/oidc/authentik/login/callback/` |
