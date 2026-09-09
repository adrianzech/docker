## Required values

| Variable | Value | Generate |
| --- | --- | --- |
| `DYNACAT_AUTH_SECRET` | Session encryption and signing secret | `openssl rand 64 \| openssl base64 -A` |
| `DYNACAT_OIDC_CLIENT_ID` | Authentik client ID | Authentik |
| `DYNACAT_OIDC_CLIENT_SECRET` | Authentik client secret | Authentik |
| `FASTMAIL_CALDAV_URL` | Fastmail calendar CalDAV URL | Fastmail |
| `FASTMAIL_USERNAME` | Fastmail account username | Fastmail |
| `FASTMAIL_APP_PASSWORD` | Fastmail app password with calendar access | Fastmail |
| `SONARR_API_KEY` | Sonarr API key | Sonarr |
| `RADARR_API_KEY` | Radarr API key | Radarr |
| `FRESHRSS_UNREAD_FEED_URL` | Authenticated FreshRSS unread-feed URL | FreshRSS |
| `FORGEJO_TOKEN` | Forgejo token with repository read access | Forgejo |
| `GRIDTIME_API_KEY` | Gridtime API key | Gridtime |
| `PAPERLESS_API_TOKEN` | Paperless API token with document read access | Paperless |
| `KARAKEEP_API_KEY` | Karakeep API key for the private smart list | Karakeep |

## Update `.env`

```bash
sed -i "s|^DYNACAT_AUTH_SECRET=.*|DYNACAT_AUTH_SECRET=$(openssl rand 64 | openssl base64 -A)|" .env
```

## Authentik OIDC

| Authentik setting | Value |
| --- | --- |
| Application/provider | Dynacat |
| Redirect URI (Strict Authorization) | `https://dashboard.zech.co/api/oidc/callback` |
