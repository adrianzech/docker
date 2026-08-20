# Speedtest Tracker

## Required values

| Variable | Value | Generate |
| --- | --- | --- |
| `DATABASE_PASSWORD` | Strong PostgreSQL password | `openssl rand -base64 32` |
| `APP_KEY` | Generated key with the `base64:` prefix | `printf 'base64:%s\n' "$(openssl rand -base64 32)"` |
| `MAIL_HOST` | SMTP server hostname | SMTP provider |
| `MAIL_PORT` | SMTP server port, usually `587` | SMTP provider |
| `MAIL_USERNAME` | SMTP username | SMTP provider |
| `MAIL_PASSWORD` | SMTP password or app password | SMTP provider |
| `MAIL_FROM_ADDRESS` | Sender address, default: `speedtest@zech.co` | — |
| `MAIL_FROM_NAME` | Sender name, default: `Speedtest Tracker` | — |

## Update `.env`

To update the local `.env` with the generated values:

```bash
sed -i "s|^DATABASE_PASSWORD=.*|DATABASE_PASSWORD=$(openssl rand -base64 32)|" .env
sed -i "s|^APP_KEY=.*|APP_KEY=base64:$(openssl rand -base64 32)|" .env
```
