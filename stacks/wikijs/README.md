## Required values

| Variable | Value | Generate |
| --- | --- | --- |
| `DB_PASS` | PostgreSQL password | `openssl rand -hex 32` |
| `ADMIN_EMAIL` | Email address for the initial Wiki.js administrator | — |
| `ADMIN_PASS` | Password for the initial Wiki.js administrator | `openssl rand -hex 32` |

## Update .env

Run these commands before the first start to fill the empty password fields.

```bash
db_password="$(openssl rand -hex 32)" &&
  sed -i "s/^DB_PASS=$/DB_PASS=$db_password/" .env
admin_password="$(openssl rand -hex 32)" &&
  sed -i "s/^ADMIN_PASS=$/ADMIN_PASS=$admin_password/" .env
```

## Authentik OIDC

Configure the Wiki.js OpenID Connect login with the following settings.

| Wiki.js setting | Value |
| --- | --- |
| Strategy | `OpenID Connect / OAuth2` |
| Display name | `Authentik` |
| Issuer | `https://sso.zech.co/application/o/wikijs/` |
| Use Discovery | Enabled |
| Scopes | `openid profile email` |
| Client ID and Client Secret | Copy from the Authentik provider into Wiki.js |
| Trust X-Forwarded-\* Proxy Headers | Enabled under **Administration → Security** |
| Site login | Assign the enabled strategy under **Administration → Login** |

| Authentik setting | Value |
| --- | --- |
| Application/provider | Wiki.js |
| Redirect URI (Strict Authorization) | Exact **Authorization Callback URL** from the Wiki.js strategy after **Apply**. It must start with `https://wiki.zech.co/`. |
| Logout URI | `https://wiki.zech.co/` |
