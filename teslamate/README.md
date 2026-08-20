# TeslaMate

## Required values

| Variable | Value | Generate |
| --- | --- | --- |
| `DATABASE_PASSWORD` | Strong PostgreSQL password | `openssl rand -base64 32` |
| `ENCRYPTION_KEY` | Persistent TeslaMate encryption key | `openssl rand -hex 32` |
| `GF_AUTH_GENERIC_OAUTH_CLIENT_ID` | Authentik client ID for TeslaMate Grafana | Authentik |
| `GF_AUTH_GENERIC_OAUTH_CLIENT_SECRET` | Authentik client secret for TeslaMate Grafana | Authentik |

## Update `.env`

To update the local `.env` with the generated values:

```bash
sed -i "s|^DATABASE_PASSWORD=.*|DATABASE_PASSWORD=$(openssl rand -base64 32)|" .env
sed -i "s|^ENCRYPTION_KEY=.*|ENCRYPTION_KEY=$(openssl rand -hex 32)|" .env
```

## Grafana Authentik OAuth

| Authentik setting | Value |
| --- | --- |
| Provider/application | TeslaMate Grafana |
| Redirect URI (Strict Authorization) | `https://teslamate-grafana.zech.co/login/generic_oauth` |
| Logout URI | `https://teslamate-grafana.zech.co/logout` |

## Grafana data-directory ownership

Run this before first deployment if needed:

```bash
sudo mkdir -p /opt/appdata/teslamate/grafana/ && \
sudo chown -R 472:472 /opt/appdata/teslamate/grafana/
```
