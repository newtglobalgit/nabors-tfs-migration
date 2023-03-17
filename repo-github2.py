import os, json, requests
from github import Github
from credentials import cred, data, commit

access_token = cred.get('token')
GITHUB_REPO = data.get('name')
commit = commit.get('message')

g = Github(access_token)
user = g.get_user()

personal_access_token = cred.get('token')
GitHub_username = cred.get('owner')
headers = {'Authorization': 'Token ' + personal_access_token}

repo_name = GITHUB_REPO
repo_description =  data.get('description')

repo_url = 'https://api.github.com/user/repos'
payload = {'name': repo_name, 'description': repo_description, 'auto_init': 'true'}

response = requests.post(repo_url, headers=headers, data=json.dumps(payload))

if response.status_code == 201:
    print('Repository created')
else:
    raise Exception('Error creating repository: {}'.format(response.content))

directory_path = data.get('directory_path')

os.chdir(directory_path)

files = {'file': open('dummy/todelete.txt', 'rb')}

upload_url = 'https://api.github.com/repos/{}/{}/contents'.format(GitHub_username, repo_name)
params = {'path': 'path_to_save_the_files'}
response = requests.put(upload_url, headers=headers, params=params, files=files)

if response.status_code == 201:
    print('Files uploaded')
else:
    raise Exception('Error uploading files: {}'.format(response.content))