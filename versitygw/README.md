# VersityGW

## Required values

| Variable | Value | Generate |
| --- | --- | --- |
| `ROOT_ACCESS_KEY` | Unique VersityGW root access key | `openssl rand -hex 16` |
| `ROOT_SECRET_KEY` | Strong, unique VersityGW root secret | `openssl rand -hex 32` |

## Update `.env`

To update the local `.env` with the generated values:

```bash
sed -i "s|^ROOT_ACCESS_KEY=.*|ROOT_ACCESS_KEY=$(openssl rand -hex 16)|" .env
sed -i "s|^ROOT_SECRET_KEY=.*|ROOT_SECRET_KEY=$(openssl rand -hex 32)|" .env
```

## Create an S3 user

Replace every placeholder below with the root credentials from `.env` and the
new user's intended access key and secret. Do not use the literal example
values as credentials.

Generate a new user's credentials separately:

```bash
openssl rand -hex 16
openssl rand -hex 32
```

Use the generated values for `<new-user-access-key>` and `<new-user-secret>`.

```bash
docker compose exec versitygw versitygw admin \
  --region eu-central-1 \
  --access <root-access-key> \
  --secret <root-secret-key> \
  --endpoint-url http://127.0.0.1:7071 create-user \
  --access <new-user-access-key> \
  --secret <new-user-secret> \
  --role admin
```
