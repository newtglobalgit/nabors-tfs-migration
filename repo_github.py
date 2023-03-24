from github import Github
import os
from credentials import cred, data

access_token = cred.get('token')

def create_repo(GITHUB_REPO):
    g = Github(access_token)
    user = g.get_user()
    repo = user.create_repo(GITHUB_REPO)
    print(f"Repository '{GITHUB_REPO}' has been created.")
