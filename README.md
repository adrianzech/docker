# Personal docker compose collection

Bellow are notes for some manual steps.

# Docker Networks

```bash
docker network create authentik && \
docker network create freshrss && \
docker network create hoarder && \
docker network create jellystat && \
docker network create monitoring && \
docker network create n8n && \
docker network create paperless && \
docker network create pgbackweb && \
docker network create proxy && \
docker network create speedtest-tracker && \
docker network create unifi
```

# Applications

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

## Grafana

Set the correct permissions for the Grafana container

```bash
sudo mkdir -p /opt/docker/appdata/grafana && \
sudo chown -R 472:472 /opt/docker/appdata/grafana
```

## Paperless

Create a admin account for Paperless

```bash
docker compose exec paperless bash
```

```bash
python3 manage.py createsuperuser
```
