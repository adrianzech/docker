# Norish

## Required values

| Variable | Value | Generate |
| --- | --- | --- |
| `DATABASE_PASSWORD` | Strong PostgreSQL password | `openssl rand -base64 32` |
| `MASTER_KEY` | Generated 32-byte Base64 key | `openssl rand -base64 32` |
| `AUTH_URL` | `https://norish.zech.co` | — |
| `OIDC_CLIENT_ID` | Authentik client ID | Authentik |
| `OIDC_CLIENT_SECRET` | Authentik client secret | Authentik |

## Update `.env`

To update the local `.env` with the generated values:

```bash
sed -i "s|^DATABASE_PASSWORD=.*|DATABASE_PASSWORD=$(openssl rand -base64 32)|" .env
sed -i "s|^MASTER_KEY=.*|MASTER_KEY=$(openssl rand -base64 32)|" .env
```

## Authentik OIDC

| Authentik setting | Value |
| --- | --- |
| Provider/application | Norish |
| Redirect URI (Strict Authorization) | `https://norish.zech.co/api/auth/oauth2/callback/oidc` |
