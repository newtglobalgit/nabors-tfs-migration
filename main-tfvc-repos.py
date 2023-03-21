from tfs import TFSAPI
from requests_ntlm import HttpNtlmAuth
from credentials import cred, server_urls, projects



user = cred.get('USER')
password = cred.get('PASSWORD')
name = projects.get('project1')
url = server_urls.get('http_url')

headers = {
    'Content-Type': 'application/json',
}

tfs = TFSAPI(url, user=user, password=password, auth_type=HttpNtlmAuth)

projects = tfs.get_projects()
for project in projects:
   print("Repo :"+project.name)
   
