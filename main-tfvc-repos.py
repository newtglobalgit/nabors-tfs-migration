from tfs import TFSAPI
from requests_ntlm import HttpNtlmAuth
from credentials import cred, server_urls, projects
import requests
import json
import subprocess

import requests
import base64
import json
#from bs4 import BeautifulSoup

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
   print(project.name)
   
#    items = tfs.get_gitrepositories("DefaultCollection", project=name)
#    for item in items:
#       print(item.server_item)


# get_tfs_items(name)



# repositories = tfs.get_gitrepositories()
# for repo in repositories:
#     print(repo.name)
#     repo_url = url+"DefaultCollection/"+repo.name
#     print(repo_url)
#     response = requests.get(repo_url)
#     print(response,"response")
#     repo_content = response.json()
#     print(repo_content['value'])



# def get_tfs_items(collection_name):
#     # Set up URL for TFS collection
#     collection_url = f"{url}DefaultCollection/{collection_name}/_versionControl"


#     # Send GET request to TFS REST API
#     response = requests.get(collection_url, auth=(user,password), headers=headers)

#     print(response.text)
#     # Parse JSON response
#     # items = json.loads(response.text)
#     items_list = response.json()['value']




#     # Return list of items
#     return items_list

# # Call function with name of TFS collection to fetch items

# items_list = get_tfs_items(name)

# for item in items_list:
#     print(item['name'])

# tfs_url = "http://<TFS server name>:8080/tfs/<collection name>/<project name>/_apis/git/repositories/<repository name>/items?scopePath=/&recursionLevel=Full&includeContentMetadata=true"




# tfs_path = 'C:\Program Files (x86)\Microsoft Visual Studio 12.0\Common7\IDE\TF.exe'
# tfs_collection_url = 'http://192.168.3.197:8080/tfs/DefaultCollection'
# workspace_path = 'C:\TFS\Practice'
# project_path = '$/name'

# cmd = [tfs_path, 'dir', workspace_path, '/recursive', '/server:{}'.format(tfs_collection_url), project_path]
# result = subprocess.run(cmd, stdout=subprocess.PIPE, universal_newlines=True)

# output = result.stdout



# set up the authentication credentials

# auth = base64.b64encode(f"{user}:{password}".encode('ascii')).decode('ascii')
# headers = {
#     "Authorization": f"Basic {auth}",
#     "Content-Type": "application/json"
# }
# repositorie= tfs.get_gitrepositories

# # set up the TFS API URL
# tfs_url = "http://192.168.3.197:8080/tfs/DefaultCollection/DPROG/_versionControl#path=%24%2Fdprog%2Finfinity.net&_a=contents"

# # send the API request to get the list of items
# response = requests.get(tfs_url, headers=headers)

# # parse the JSON response and print the list of item paths
# items = response.json()['value']
# for item in items:
#     print(item['path'])
