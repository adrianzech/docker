# Sonarr

## External authentication

Edit `/opt/appdata/sonarr/config/config.xml`

In Sonarr's authentication settings, use the following XML values for external
authentication while allowing local-address access:

```xml
<AuthenticationMethod>External</AuthenticationMethod>
<AuthenticationRequired>DisabledForLocalAddresses</AuthenticationRequired>
```
