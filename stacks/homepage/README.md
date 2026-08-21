## Required values

| Variable | Value | Generate |
| --- | --- | --- |
| `HOMEPAGE_AUTH_SECRET` | Cookie encryption and signing secret | `openssl rand -base64 32` |
| `HOMEPAGE_OIDC_CLIENT_ID` | Authentik client ID | Authentik |
| `HOMEPAGE_OIDC_CLIENT_SECRET` | Authentik client secret | Authentik |

## Widget values

Add the existing application API keys, tokens, and credentials listed in
`.env.example` as `HOMEPAGE_VAR_*` values. Homepage substitutes these values
in the untracked configuration under `../../appdata/homepage/config`; no
credential is stored in the repository.

## Update `.env`

```bash
sed -i "s|^HOMEPAGE_AUTH_SECRET=.*|HOMEPAGE_AUTH_SECRET=$(openssl rand -base64 32)|" .env
```

## Authentik OIDC

| Authentik setting | Value |
| --- | --- |
| Provider/application | Homepage |
| Redirect URI (Strict Authorization) | `https://dashboard.zech.co/api/auth/callback/homepage-oidc` |
