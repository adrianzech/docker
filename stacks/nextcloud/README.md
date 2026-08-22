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

## Single Sign On (SSO)

### Authentik OIDC

| Authentik setting | Value |
| --- | --- |
| Provider/application | Nextcloud |
| Redirect URI (Strict Authorization) | `https://cloud.zech.co/apps/user_oidc/code` |
| Logout URL | `https://cloud.zech.co/apps/user_oidc/backchannel-logout/Authentik` |

### Nextcloud configuration

Install the OpenID Connect app and allow the container to connect to the local Authentik instance:

```bash
docker compose exec --user www-data nextcloud php occ app:install user_oidc
docker compose exec --user www-data nextcloud php occ config:system:set allow_local_remote_servers --value=true --type=boolean
```

Configure the provider with the client ID and client secret from Authentik:

```bash
docker compose exec --user www-data nextcloud \
  php occ user_oidc:provider Authentik \
  --clientid='client_id' \
  --clientsecret='client_secret' \
  --discoveryuri='https://sso.zech.co/application/o/nextcloud/.well-known/openid-configuration' \
  --scope='openid profile email'
```

### Use OIDC as the default login method

```bash
docker compose exec --user www-data nextcloud php occ config:app:set --type=string --value=0 user_oidc allow_multiple_user_backends
```

### Fallback URL

`https://cloud.zech.co/login?direct=1`
