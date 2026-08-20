# Immich

## Required values

| Variable | Value | Generate |
| --- | --- | --- |
| `DATABASE_PASSWORD` | Strong PostgreSQL password | `openssl rand -base64 32` |

## Update `.env`

To update the local `.env` with the generated values:

```bash
sed -i "s|^DATABASE_PASSWORD=.*|DATABASE_PASSWORD=$(openssl rand -base64 32)|" .env
```

## Authentik OIDC

Configure the Immich OpenID Connect login with the following settings.

| Immich setting | Value |
| --- | --- |
| `issuer_url` | `https://sso.zech.co/application/o/immich/` |
| `scope` | `openid email profile` |
| Button text | `Authentik` |

| Authentik setting | Value |
| --- | --- |
| Provider/application | Immich |
| Redirect URI (Strict Authorization) | `app.immich:///oauth-callback` |
| Redirect URI (Strict Authorization) | `https://photos.zech.co/auth/login` |
| Redirect URI (Strict Authorization) | `https://photos.zech.co/user-settings` |
| Launch URL | `https://photos.zech.co/auth/login?autoLaunch=1` |
