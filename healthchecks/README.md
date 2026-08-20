# Healthchecks

## Required values

| Variable | Value | Generate |
| --- | --- | --- |
| `DATABASE_PASSWORD` | Strong PostgreSQL password | `openssl rand -base64 32` |
| `SECRET_KEY` | Persistent Django secret key | `openssl rand -base64 64` |
| `EMAIL_HOST` | SMTP server hostname | SMTP provider |
| `EMAIL_HOST_USER` | SMTP username | SMTP provider |
| `EMAIL_HOST_PASSWORD` | SMTP password or app password | SMTP provider |
| `PUSHOVER_API_TOKEN` | Pushover API token, if used | Pushover |

## Update `.env`

To update the local `.env` with the generated values:

```bash
sed -i "s|^DATABASE_PASSWORD=.*|DATABASE_PASSWORD=$(openssl rand -base64 32)|" .env
sed -i "s|^SECRET_KEY=.*|SECRET_KEY=$(openssl rand -base64 64)|" .env
```
