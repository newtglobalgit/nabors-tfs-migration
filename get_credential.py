import hvac

# Create a Vault client and authenticate using a token
client = hvac.Client(url='http://127.0.0.1:8200')
client.token = 'hvs.uqtNdaqI7Duo3kIY9OwsGgNT'

# Retrieve the username and password from a secret named 'mysecret'
secret = client.secrets.kv.v2.read_secret_version(path='tfsserver')

username = secret['data']['data']['username']
password = secret['data']['data']['password']

# Use the username and password for further processing
print(f"Username: {username}")
print(f"Password: {password}")