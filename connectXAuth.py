from oauthlib.oauth1 import Client, SIGNATURE_TYPE_BODY
from oauthlib.common import urldecode
import requests
import sys

CONTENT_TYPE_FORM_URLENCODED = 'application/x-www-form-urlencoded'

hostname = "musescore.com"

request_token_url = 'https://api.' + hostname+'/oauth/request_token'
base_authorization_url = 'https://' + hostname+'/oauth/authorize'
access_token_url = 'https://api.' + hostname+'/oauth/access_token'

#----- PLEASE CHANGE THESE VARIABLES -----
client_key = 'YOUR_CLIENT_KEY'
client_secret = 'YOUR_CLIENT_SECRET'
username = 'USER_NAME'
password = 'USER_PASSWORD'
#-----------------------------------------

resource_owner_key = ''
resource_owner_secret = ''

if client_key == '' or client_secret == '':
    print "Please change your client key and secret in connectXAuth.py header"
    sys.exit(0)

if username == 'USER_NAME' or password == 'USER_PASSWORD':
    print "Please change username and password in connectXAuth.py header"
    sys.exit(0)

client = Client(client_key, client_secret=client_secret, signature_type=SIGNATURE_TYPE_BODY)
headers = {"Content-Type": CONTENT_TYPE_FORM_URLENCODED}
body = 'x_auth_mode=client_auth&x_auth_username='+username+'&x_auth_password='+password
result = client.sign(access_token_url, http_method="POST", headers=headers, body=body)

data = result[2]
r = requests.post(access_token_url, headers=headers, data=data)

oauth_tokens = dict(urldecode(r.text.strip()))

resource_owner_key = oauth_tokens.get('oauth_token')
resource_owner_secret = oauth_tokens.get('oauth_token_secret')

cred = {"client_key": client_key, "client_secret": client_secret,
        "resource_owner_key": resource_owner_key,
        "resource_owner_secret": resource_owner_secret}

import json
with open('credentials.json', 'w') as outfile:
    json.dump(cred, outfile)
