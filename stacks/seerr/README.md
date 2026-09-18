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

| Authentik setting | Value |
| --- | --- |
| Provider/application | Seerr |
| Redirect URI (Strict Authorization) | `https://seerr.zech.co/login` |
| Redirect URI (Strict Authorization) | `https://seerr.zech.co//profile/settings/linked-accounts` |

Keep `ghcr.io/seerr-team/seerr:preview-new-oidc` configured until OIDC support is available in a stable Seerr image. Add the following provider to `../../appdata/seerr/config/settings.json`, then set the client ID and secret from the Authentik provider:

```json
{
  "oidc": {
    "providers": [
      {
        "slug": "authentik",
        "name": "Authentik",
        "issuerUrl": "https://sso.zech.co/application/o/seerr/.well-known/openid-configuration",
        "clientId": "",
        "clientSecret": "",
        "logo": "https://sso.zech.co/static/dist/assets/icons/icon.png"
      }
    ]
  }
}
```
