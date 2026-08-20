# SABnzbd

## Download-directory permissions

The container runs as UID and GID `1000`. Before deployment, ensure the
incomplete and complete download directories are owned and writable by that
user and group:

```bash
sudo chown -R 1000:1000 /mnt/downloads/incomplete /mnt/downloads/complete
sudo find /mnt/downloads/incomplete /mnt/downloads/complete -type d -exec chmod 775 {} \;
sudo find /mnt/downloads/incomplete /mnt/downloads/complete -type f -exec chmod 664 {} \;
```

These commands affect the two specified download trees recursively. Review the
paths before running them on a host with existing downloads.
