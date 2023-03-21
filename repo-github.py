from github import Github
import os
from credentials import cred, data
access_token = cred.get('token')
GITHUB_REPO = data.get('name')
g = Github(access_token)
folder_prefix = "Asii/"
user = g.get_user()
repo = user.create_repo(GITHUB_REPO)
print(f"Repository '{GITHUB_REPO}' has been created.")
folder_path ="Asii"
os.chdir(folder_path)
print(f"Current working directory: {os.getcwd()}")
for file_name in os.listdir('.'):
    with open(file_name, 'rb') as file:
        content = file.read()
        repo.create_file(folder_prefix + file_name, f"Committing {file_name}", content)
        print(f"{file_name} uploaded to {GITHUB_REPO} with prefix '{folder_prefix}'.")
print("All files have been uploaded successfully.")


# from github import Github
# from git import Repo
# import os
# from credentials import cred, data

# access_token = cred.get('token')
# GITHUB_REPO = data.get('name')

# # Authenticate with GitHub API
# g = Github(access_token)

# # Create repository
# user = g.get_user()
# repo = user.create_repo(GITHUB_REPO)
# print(f"Repository '{GITHUB_REPO}' has been created.")

# # Initialize Git LFS
# repo_path = f"{os.getcwd()}\{GITHUB_REPO}"
# repo = Repo.init(repo_path)
# git_lfs = repo.git('install')

# # Add files to Git LFS
# folder_prefix = "Asii/"
# for file_name in os.listdir('.'):
#     file_path = os.path.join("C:/TFS/tfs-test/GitHubDesktopSetup-x64.exe", file_name)
#     if os.path.isfile(file_path):
#         repo.index.add([file_path])
#         print(f"{file_name} added to index.")

# # Commit changes to Git LFS
# commit_msg = "Add files to Git LFS"
# repo.index.commit(commit_msg)

# # Push changes to GitHub
# origin = repo.remote(name='origin')
# origin.push()
# print("All files have been uploaded successfully.")


# from github import Github
# from git import Repo
# import os
# from credentials import cred, data

# access_token = cred.get('token')
# GITHUB_REPO = data.get('name')

# # Authenticate with GitHub API
# g = Github(access_token)

# # Create repository
# user = g.get_user()
# repo = user.create_repo(GITHUB_REPO)
# print(f"Repository '{GITHUB_REPO}' has been created.")

# # Initialize Git LFS
# repo_path = f"{os.getcwd()}/{GITHUB_REPO}"
# repo = Repo.init(repo_path)
# git_lfs = repo.git.execute(['git', 'lfs', 'install'])

# # Add files to Git LFS
# folder_prefix = "Asii/"
# for file_name in os.listdir('.'):
#     # file_path = os.path.join("C:/TFS/tfs-test/GitHubDesktopSetup-x64.exe", file_name)
#     file_path = "C:\\TFS\\Demo\\tfs-migration12\\GitHubDesktopSetup-x64.exe"
#     if os.path.isfile(file_path):
#         repo.index.add([file_path])
#         print(f"{file_name} added to index.")

# # Commit changes to Git LFS
# commit_msg = "Add files to Git LFS"
# repo.index.commit(commit_msg)

# # Push changes to GitHub
# origin = repo.remote(name='master')
# origin.push()
# print("All files have been uploaded successfully.")



