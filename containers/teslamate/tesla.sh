CLIENT_ID=1451edcf-045c-4503-bc89-0ed8fbbd6e21
CLIENT_SECRET=ta-secret.kIPPLi%!oJ2Bo!qz
AUDIENCE="https://fleet-api.prd.eu.vn.cloud.tesla.com"
curl --request POST \
  --header 'Content-Type: application/x-www-form-urlencoded' \
  --data-urlencode 'grant_type=client_credentials' \
  --data-urlencode "client_id=$CLIENT_ID" \
  --data-urlencode "client_secret=$CLIENT_SECRET" \
  --data-urlencode 'scope=openid vehicle_device_data vehicle_cmds vehicle_charging_cmds' \
  --data-urlencode "audience=$AUDIENCE" \
  'https://fleet-auth.prd.vn.cloud.tesla.com/oauth2/v3/token'
