# Radarr

## External authentication

Edit `../../appdata/radarr/config/config.xml`

In Radarr's authentication settings, use the following XML values for external
authentication while allowing local-address access:

```xml
<AuthenticationMethod>External</AuthenticationMethod>
<AuthenticationRequired>DisabledForLocalAddresses</AuthenticationRequired>
```
