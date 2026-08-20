# Karakeep

## Required values

| Variable | Value | Generate |
| --- | --- | --- |
| `NEXTAUTH_URL` | `https://karakeep.zech.co` | — |
| `NEXTAUTH_SECRET` | Generated JWT signing secret | `openssl rand -base64 36` |
| `MEILI_MASTER_KEY` | Generated Meilisearch master key | `openssl rand -base64 36 \| tr -dc 'A-Za-z0-9'` |
| `OPENAI_API_KEY` | OpenAI API key | External |
| `SMTP_HOST` | SMTP host | External |
| `SMTP_USER` | SMTP username | External |
| `SMTP_PASSWORD` | SMTP password | External |
| `OAUTH_WELLKNOWN_URL` | Authentik provider discovery URL | Authentik |
| `OAUTH_CLIENT_ID` | Authentik client ID | Authentik |
| `OAUTH_CLIENT_SECRET` | Authentik client secret | Authentik |

## Update `.env`

To update the local `.env` with the generated values:

```bash
sed -i "s|^NEXTAUTH_SECRET=.*|NEXTAUTH_SECRET=$(openssl rand -base64 36)|" .env
sed -i "s|^MEILI_MASTER_KEY=.*|MEILI_MASTER_KEY=$(openssl rand -base64 36 | tr -dc 'A-Za-z0-9')|" .env
```

## Authentik OIDC

Create an OAuth2/OpenID provider for Karakeep and set its discovery URL, client
ID, and client secret in the OAUTH variables above.

| Authentik setting | Value |
| --- | --- |
| Provider/application | Karakeep |
| Redirect URI (Strict Authorization) | `https://karakeep.zech.co/api/auth/callback/custom` |
