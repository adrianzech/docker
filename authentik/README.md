# Authentik

## Required values

| Variable | Value | Generate |
| --- | --- | --- |
| `DATABASE_PASSWORD` | Strong PostgreSQL password | `openssl rand -base64 32` |
| `AUTHENTIK_SECRET_KEY` | Persistent Authentik secret key | `openssl rand -base64 64` |
| `AUTHENTIK_EMAIL__HOST` | SMTP server hostname | SMTP provider |
| `AUTHENTIK_EMAIL__USERNAME` | SMTP username | SMTP provider |
| `AUTHENTIK_EMAIL__PASSWORD` | SMTP password or app password | SMTP provider |
| `AUTHENTIK_EMAIL__FROM` | Sender address, default: `sso@zech.co` | — |

## Update `.env`

To update the local `.env` with the generated values:

```bash
sed -i "s|^DATABASE_PASSWORD=.*|DATABASE_PASSWORD=$(openssl rand -base64 32)|" .env
sed -i "s|^AUTHENTIK_SECRET_KEY=.*|AUTHENTIK_SECRET_KEY=$(openssl rand -base64 64)|" .env
```
