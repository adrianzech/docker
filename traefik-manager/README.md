# Traefik Manager

## Authentik OIDC

Configure an OAuth2/OpenID provider for Traefik Manager with the following
redirect URI. The client ID and client secret are configured in Traefik Manager
itself, not through this Compose stack.

| Authentik setting | Value |
| --- | --- |
| Provider/application | Traefik Manager |
| Redirect URI (Strict Authorization) | `https://traefik-manager.zech.co/auth/oidc/callback` |
