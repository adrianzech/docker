# Profilarr

## Required values

| Variable | Value | Generate |
| --- | --- | --- |
| `OIDC_CLIENT_ID` | Authentik client ID | Authentik |
| `OIDC_CLIENT_SECRET` | Authentik client secret | Authentik |

## Authentik OIDC

| Authentik setting | Value |
| --- | --- |
| Provider/application | Profilarr |
| Redirect URI (Strict Authorization) | `https://profilarr.zech.co/auth/oidc/callback` |
