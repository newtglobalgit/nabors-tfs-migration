import requests, logging, sys, json
from asyncio.log import logger
from requests_ntlm import HttpNtlmAuth
from credentials import cred, urls, projects

username = cred.get('USER')
password = cred.get('PASSWORD')

url = urls.get('http_url')

headers = {
    'Content-Type': 'application/json',
}

response = requests.get(url, headers=headers, auth=HttpNtlmAuth(username, password), verify=False)
logger.info(print(f"TFS Authentication for User {username} is successful"))

projects = response.json()

name = [project['name'] for project in projects['value']]

print('Projects: ', name)

