# FreshRSS

## Required values

| Variable | Value | Generate |
| --- | --- | --- |
| `DATABASE_PASSWORD` | Strong PostgreSQL password | `openssl rand -base64 32` |
| `PUID` | Host user ID, default: `1000` | — |
| `PGID` | Host group ID, default: `1000` | — |
| `TZ` | `Europe/Vienna` | — |

## Update `.env`

To update the local `.env` with the generated values:

```bash
sed -i "s|^DATABASE_PASSWORD=.*|DATABASE_PASSWORD=$(openssl rand -base64 32)|" .env
```
