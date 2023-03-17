from github import Github
import os
from credentials import cred, data

access_token = cred.get('token')
GITHUB_REPO = data.get('name')
dir = data.get('directory_path')

g = Github(access_token)

folder_prefix = dir+"/"

user = g.get_user()
repo = user.create_repo(GITHUB_REPO)
print(f"Repository '{GITHUB_REPO}' has been created.")
folder_path = dir
os.chdir(folder_path)

print(f"Current working directory: {os.getcwd()}")

for file_name in os.listdir('.'):
    with open(file_name, 'rb') as file:
        content = file.read()
        repo.create_file(folder_prefix + file_name, f"Committing {file_name}", content)
        print(f"{file_name} uploaded to {GITHUB_REPO} with prefix '{folder_prefix}'.")

print("All files have been uploaded successfully.")