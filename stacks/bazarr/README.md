# Bazarr

## External authentication

Edit `../../appdata/bazarr/config/config.xml`

In Bazarr's authentication settings, use the following XML values for external
authentication while allowing local-address access:

```xml
<AuthenticationMethod>External</AuthenticationMethod>
<AuthenticationRequired>DisabledForLocalAddresses</AuthenticationRequired>
```
