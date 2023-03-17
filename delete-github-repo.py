import os
import requests
from credentials import cred, data

access_token = cred.get('token')
organization = cred.get('owner')
GITHUB_REPO = data.get('name')

url = 'https://api.github.com/repos/{}'.format(organization)
headers = {'Accept': 'application/vnd.github.v3+json',
           'Authorization': 'token {}'.format(access_token)}

lines = [line.strip() for line in open('todelete.txt')]
for repo in lines:
    print(os.path.join(url, repo))
    deleterequest = requests.delete(os.path.join(url, repo), headers=headers)
    print(deleterequest.content)