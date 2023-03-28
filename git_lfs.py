import requests
import repo_github
import get_list_of_branch
from credentials import cred, server, path, server_urls 


url = server.get('host')
server_url = url+':8000/one'
response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    print(data['message'])
else:
    print(f'Error: {response.status_code} - {response.text}')

