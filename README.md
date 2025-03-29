# 🐳 Docker Compose Collection

A personal Docker Compose collection to easily deploy and manage various self-hosted applications on a Linux system.

## 🚀 Features

- **Modular Structure**: Each application has its own directory with compose file and environment configuration
- **GitHub Actions Workflow**: Automatic deployment when changes are pushed to the main branch
- **Network Segmentation**: Applications are isolated in their own Docker networks where appropriate
- **Easy Configuration**: Environment templates (.env.dist) provided for all services requiring configuration

## 🔧 Initial Setup

### Create Required Docker Networks

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

### Clone the Repository

```bash
git clone https://github.com/yourusername/docker-compose-collection.git /opt/docker
cd /opt/docker
```

### Configure Applications

1. Navigate to the container directory of the application you want to deploy
2. Copy the template environment file:
   ```bash
   cp .env.dist .env
   ```
3. Edit the `.env` file to set your configurations, passwords, and secrets

## 🚢 Deploying Applications

To deploy an application:

```bash
cd /opt/docker/containers/[application-name]
docker compose up -d
```

## 🔄 Auto-Deploy with GitHub Actions

This repository includes a GitHub Actions workflow that automatically deploys changes when pushed to the main branch:

1. Set up a self-hosted GitHub Actions runner on your server
2. Add the following secrets to your GitHub repository:
   - `SSH_PRIVATE_KEY`: SSH key to connect to your server
   - `SSH_USER`: Username for SSH connection
   - `SSH_HOST`: Hostname or IP address of your server
3. Push changes to the main branch to trigger deployments

The workflow will:
- Detect which container directories have changed
- Pull the latest images for those containers
- Recreate and restart the affected containers

## 📦 Included Applications

| Category | Application | Description |
|----------|-------------|-------------|
| **Authentication** | Authentik | Modern SSO identity provider |
| **Media** | Bazarr | Subtitle management |
|  | Jellyseerr | Request management for media servers |
|  | Jellystat | Statistics for Jellyfin |
|  | Radarr | Movie management |
|  | Sonarr | TV show management |
| **Download** | Prowlarr | Indexer management |
|  | qBittorrent | Torrent client |
|  | SABnzbd | Usenet downloader |
|  | YouTube-DL | YouTube downloader |
| **Documents** | Paperless-ngx | Document management system |
|  | Stirling-PDF | PDF manipulation tools |
| **Productivity** | FreshRSS | RSS feed reader |
|  | Ghost | Blogging platform |
|  | Healthchecks | Cron job monitoring |
|  | n8n | Workflow automation |
| **Monitoring** | Beszel | Server monitoring |
|  | ChangeDetection | Web page change detection |
|  | Grafana | Dashboards and visualization |
|  | Node-Exporter | System metrics exporter |
|  | Prometheus | Monitoring system |
|  | Speedtest-Tracker | Internet speed tracking |
|  | Teslamate | Tesla vehicle logging and tracking |
| **Development** | Code-Server | VS Code in the browser |
|  | IT-Tools | Various IT utilities |
| **Finance** | Wallos | Subscription management |
| **Utility** | Doku | Docker management UI |
|  | Homepage | Application dashboard |
|  | Hoarder | Web page archiver |
|  | LinkStack | Link sharing page |
|  | Pingvin-Share | File sharing solution |
|  | Portainer | Container management |
|  | PgBackWeb | PostgreSQL backup manager |

## 📝 Special Setup Notes

### Linkstack

```bash
cd /opt/docker/appdata/linkstack && \
wget https://github.com/linkstackorg/linkstack/releases/latest/download/linkstack.zip && \
unzip linkstack.zip && \
mv linkstack htdocs && \
rm linkstack.zip README.md
sed -i 's\FORCE_HTTPS=false\FORCE_HTTPS=true\g' /opt/docker/appdata/linkstack/htdocs/.env
sudo chown -R 100:101 /opt/docker/appdata/linkstack
```

### Grafana

```bash
sudo mkdir -p /opt/docker/appdata/grafana && \
sudo chown -R 472:472 /opt/docker/appdata/grafana
```

### Paperless

Create admin account:
```bash
docker compose exec paperless bash
python3 manage.py createsuperuser
```

## 🔒 Security Notes

- All sensitive information (passwords, API keys, etc.) should be stored in `.env` files which are excluded from Git via `.gitignore`
- Use strong, unique passwords for all services
- Consider implementing proper backups for important data
- Review and customize container networking as needed for your environment


