# Nextcloud

## Required values

| Variable | Value | Generate |
| --- | --- | --- |
| `DATABASE_PASSWORD` | Strong PostgreSQL password | `openssl rand -base64 32` |
| `NEXTCLOUD_ADMIN_USER` | Initial administrator username | — |
| `NEXTCLOUD_ADMIN_PASSWORD` | Initial administrator password | `openssl rand -base64 32` |
| `SMTP_NAME` | SMTP username | SMTP provider |
| `SMTP_PASSWORD` | SMTP password or app password | SMTP provider |
| `EUROOFFICE_JWT_SECRET` | Persistent Euro Office JWT secret | `openssl rand -hex 32` |

## Update `.env`

To update the local `.env` with the generated values:

```bash
sed -i "s|^DATABASE_PASSWORD=.*|DATABASE_PASSWORD=$(openssl rand -base64 32)|" .env
sed -i "s|^NEXTCLOUD_ADMIN_PASSWORD=.*|NEXTCLOUD_ADMIN_PASSWORD=$(openssl rand -base64 32)|" .env
sed -i "s|^EUROOFFICE_JWT_SECRET=.*|EUROOFFICE_JWT_SECRET=$(openssl rand -hex 32)|" .env
```
