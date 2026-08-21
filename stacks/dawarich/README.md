# Dawarich

## Required values

| Variable | Value | Generate |
| --- | --- | --- |
| `DATABASE_PASSWORD` | Strong PostgreSQL password | `openssl rand -base64 32` |
| `SECRET_KEY_BASE` | Generated Rails secret | `openssl rand -hex 64` |
| `OIDC_CLIENT_ID` | Authentik client ID | Authentik |
| `OIDC_CLIENT_SECRET` | Authentik client secret | Authentik |

## Update `.env`

To update the local `.env` with the generated values:

```bash
sed -i "s|^DATABASE_PASSWORD=.*|DATABASE_PASSWORD=$(openssl rand -base64 32)|" .env
sed -i "s|^SECRET_KEY_BASE=.*|SECRET_KEY_BASE=$(openssl rand -hex 64)|" .env
```

## Authentik OIDC

| Authentik setting | Value |
| --- | --- |
| Provider/application | Dawarich |
| Redirect URI (Strict Authorization) | `https://dawarich.zech.co/users/auth/openid_connect/callback` |
