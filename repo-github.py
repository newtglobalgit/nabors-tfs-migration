from github import Github
import os
from credentials import cred, data

access_token = cred.get('token')
GITHUB_REPO = data.get('name')

g = Github(access_token)

user = g.get_user()
repo = user.create_repo(GITHUB_REPO)
all_files = []

print(f"Repository '{GITHUB_REPO}' has been created.")

folder_path = "dummies"
os.chdir(folder_path)
print(f"Current working directory: {os.getcwd()}")

git_prefix = 'dummy/'
git_file = git_prefix + 'file.txt'
for file_name in os.listdir('.'):
    with open(file_name, 'r') as file:
        content = file.read()
if git_file in all_files:
    contents = repo.get_contents(git_file)
    repo.update_file(contents.path, "committing files", content, contents.sha, branch="main")
    print(git_file + ' UPDATED')
else:
    repo.create_file(git_file, "committing files", content, branch="main")
    print(git_file + ' CREATED')
for file_name in os.listdir('.'):
    with open(file_name, 'r') as file:
        content = file.read()
        repo.create_file(file_name, f"Committing {file_name}", content)
        print(f"{file_name} uploaded to {GITHUB_REPO}.")
print("temp file has been uploaded successfully.")
contents = repo.get_contents("")

while contents:
    file_content = contents.pop(0)
    if file_content.type == "dir":
        contents.extend(repo.get_contents(file_content.path))
    else:
        file = file_content
        all_files.append(str(file).replace('ContentFile(path="','').replace('")',''))

print("directory is uploaded")