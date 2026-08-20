# Prowlarr

## External authentication

Edit `/opt/appdata/prowlarr/config/config.xml`

In Prowlarr's authentication settings, use the following XML values for
external authentication while allowing local-address access:

```xml
<AuthenticationMethod>External</AuthenticationMethod>
<AuthenticationRequired>DisabledForLocalAddresses</AuthenticationRequired>
```
