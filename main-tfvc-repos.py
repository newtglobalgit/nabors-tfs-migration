from tfs import TFSAPI
from requests_ntlm import HttpNtlmAuth
from credentials import cred, server_urls, projects
import requests
#from bs4 import BeautifulSoup

user = cred.get('USER')
password = cred.get('PASSWORD')
name = projects.get('project3')
url = server_urls.get('http_url')

headers = {
    'Content-Type': 'application/json',
}

tfs = TFSAPI(url, user=user, password=password, auth_type=HttpNtlmAuth)

projects = tfs.get_projects()
#for project in projects:
#    print(project.name)

repositories = tfs.get_gitrepositories()

for repo in repositories:
    print(repo.name)
    repo_url = url+"DefaultCollection/_git/"+repo.name
    print(repo_url)

    response = requests.get(repo_url)
    repo_content = response.json()
    print(repo_content['value'])