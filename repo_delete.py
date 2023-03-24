from github import Github 
from credentials import cred, data 
access_token = cred.get('token') 
# GITHUB_REPO = data.get('name') 
GITHUB_REPO = data.get('name') 
g = Github(access_token) 
target_repo = data.get('name') 
repo = g.get_user().get_repo(target_repo) 
repo.delete() 
print("repo deleted")