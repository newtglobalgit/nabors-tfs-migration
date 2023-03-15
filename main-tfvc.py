# List all repositories in TFS REST API
import requests, logging, sys, json
from asyncio.log import logger
from requests_ntlm import HttpNtlmAuth
from credentials import cred, urls, projects

username = cred.get('USER')
password = cred.get('PASSWORD')

url = urls.get('http_url')
project = projects.get('project1')

headers = {
    'Content-Type': 'application/json',
}

response = requests.get(url, headers=headers, auth=HttpNtlmAuth(username, password), verify=False)
logger.info(print(f"TFS Authentication for User {username} is successful"))

projects = response.json()

name = [project['name'] for project in projects['value']]

print('Projects: ', name)
#logger.info(print(f"Found TFS repos for User: {username}"))

""" for repository in repositories:
    logger.info(print(f"TFS repo for Project: {project}"))
    print(repository['name'])
 """
""" if response.status_code == 200:
    logger.info(print(f"Found TFS repos for User: {username}"))
    repositories = response.json()
    for repository in repositories['value']:
        logger.info(print(f"TFS repo for Project: {project}"))
        print(repository['name']) """