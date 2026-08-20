# Tracearr

## Required values

| Variable | Value | Generate |
| --- | --- | --- |
| `DATABASE_PASSWORD` | Strong PostgreSQL password | `openssl rand -base64 32` |
| `JWT_SECRET` | Generated 32-byte hexadecimal value | `openssl rand -hex 32` |
| `COOKIE_SECRET` | Generated 32-byte hexadecimal value | `openssl rand -hex 32` |
| `BETTER_AUTH_SECRET` | Generated 32-byte hexadecimal value | `openssl rand -hex 32` |
| `OIDC_CLIENT_ID` | Authentik client ID | Authentik |
| `OIDC_CLIENT_SECRET` | Authentik client secret | Authentik |

## Update `.env`

To update the local `.env` with the generated values:

```bash
sed -i "s|^DATABASE_PASSWORD=.*|DATABASE_PASSWORD=$(openssl rand -base64 32)|" .env
sed -i "s|^JWT_SECRET=.*|JWT_SECRET=$(openssl rand -hex 32)|" .env
sed -i "s|^COOKIE_SECRET=.*|COOKIE_SECRET=$(openssl rand -hex 32)|" .env
sed -i "s|^BETTER_AUTH_SECRET=.*|BETTER_AUTH_SECRET=$(openssl rand -hex 32)|" .env
```

## Authentik OIDC

| Authentik setting | Value |
| --- | --- |
| Provider/application | Tracearr |
| Redirect URI (Strict Authorization) | `https://tracearr.zech.co/api/v1/auth/oauth2/callback/oidc` |
