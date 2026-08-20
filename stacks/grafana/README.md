# Grafana

## Required values

| Variable | Value | Generate |
| --- | --- | --- |
| `GF_AUTH_GENERIC_OAUTH_CLIENT_ID` | Authentik client ID | Authentik |
| `GF_AUTH_GENERIC_OAUTH_CLIENT_SECRET` | Authentik client secret | Authentik |

## Authentik OAuth

| Authentik setting | Value |
| --- | --- |
| Provider/application | Grafana |
| Redirect URI (Strict Authorization) | `https://grafana.zech.co/login/generic_oauth` |
| Logout URI | `https://grafana.zech.co/logout` |

## Data-directory ownership

Run this before the first deployment if the host path does not already belong
to Grafana's container user:

```bash
sudo mkdir -p ../../appdata/grafana/ && \
sudo chown -R 472:472 ../../appdata/grafana/
```
