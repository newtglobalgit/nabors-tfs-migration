# Set up authentication credentials and base URL

from credentials import cred, server, path
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication

# Set up the connection to the TFS collection
username = cred.get('USER')
password = cred.get('PASSWORD')
base_url = server.get('host')


# Connect to TFS server
tfs_url = "http://192.168.3.197:8080/tfs/DefaultCollection"
user = username
token = password
credentials = BasicAuthentication(user, token)
connection = Connection(base_url=tfs_url, creds=credentials)
print(connection)

# Get list of all items in repository
client = connection.clients.get_tfvc_client()
items = client.get_items()

# Find the file you're interested in
file_name = "file.py"
file_path = None
for item in items:
    if item.is_item_file() and item.path.endswith(file_name):
        file_path = item.path
        break

if file_path is None:
    print("File not found in repository.")
else:
    print("File path:", file_path)
