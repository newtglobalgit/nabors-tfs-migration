import hvac

# create a Vault client object
client = hvac.Client(url='http://127.0.0.1:8200', token='hvs.1mfOeI2iSOSM23KsshFQXRjj')

# retrieve the secret containing the username and password
secret = client.secrets.kv.v2.read_secret_version(path='secret/data/tfsserver')

# extract the username and password from the secret
username = secret['data']['username']
password = secret['data']['password']