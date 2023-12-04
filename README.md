# Personal docker compose collection

Bellow are some notes for some manual steps.

# Networks

```bash
docker network create proxy && \
docker network create authentik && \
docker network create freshrss && \
docker network create speedtest-tracker && \
docker network create paperless && \
docker network create guacamole && \
docker network create kitchenowl && \
docker network create tandoor && \
docker network create unifi
```

# Applications

## Traefik

Create acme.json file and set the correct permissions to store the certificates

```bash
touch /opt/docker/appdata/traefik/acme.json && sudo chmod 600 /opt/docker/appdata/traefik/acme.json
```

## Linkstack
```bash
cd /opt/docker/appdata/linkstack && \
wget https://github.com/linkstackorg/linkstack/releases/latest/download/linkstack.zip && \
unzip linkstack.zip && \
mv linkstack htdocs && \
rm linkstack.zip README.md
sed -i 's\FORCE_HTTPS=false\FORCE_HTTPS=true\g' /opt/docker/appdata/linkstack/htdocs/.env
sudo chown -R 100:101 /opt/docker/appdata/linkstack
```

## pgAdmin

Set the correct permissions for the pgAdmin container

```bash
sudo touch pgadmin/config_local.py && sudo chown -R 5050:5050 pgadmin
```

## Guacamole
Export initdb.sql -> Import into Postgresql Database -> Comment MFA config -> Start Container and create user with the same e-mail as in Authentik -> uncomment MFA config -> Restart container

Default Login: guacadmin / guacadmin

```bash
docker run --rm guacamole/guacamole /opt/guacamole/bin/initdb.sh --postgresql > initdb.sql
docker exec -i guacamole-database psql -U guacamole -d guacamole < initdb.sql
```
## Grafana

Set the correct permissions for the Grafana container

```bash
sudo mkdir -p /opt/docker/appdata/grafana && \
sudo chown -R 472:472 /opt/docker/appdata/grafana
```

## Tandoor
ENABLE_SIGNUP=0
https://tandoor.example.org/accounts/authentik/login/callback/

## Paperless

Create a admin account for Paperless

```bash
docker compose exec paperless bash
```

```bash
python3 manage.py createsuperuser
```

# Nextcloud 
```bash
vim nextcloud/nextcloud/config/www/nextcloud/config/config.php
```
Add
```
'memcache.distributed' => '\OC\Memcache\Redis',
'redis' => [
  'host' => 'nextcloud-redis',
  'port' => 6379,
],
'overwriteprotocol' => 'https',
'default_phone_region' => 'AT',
'trusted_domains' =>
array (
  0 => 'cloud.zech.co',
),
'trusted_proxies' =>
array (
  0 => '10.0.10.100',
),
```

```bash
vim nextcloud/nextcloud/config/nginx/site-confs/default.conf
```

Add
```nginx
fastcgi_read_timeout 600;
fastcgi_send_timeout 600;
fastcgi_connect_timeout 600;
proxy_connect_timeout 600;
proxy_send_timeout 600;
proxy_read_timeout 600;
send_timeout 600;
```

Under
```nginx
location ~ \.php(?:$|/)
```