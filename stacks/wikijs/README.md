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
