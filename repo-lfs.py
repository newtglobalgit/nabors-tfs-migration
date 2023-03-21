import git
from github import Github
import os
from credentials import cred, data


access_token = cred.get('token')
GITHUB_REPO = data.get('name')
g = Github(access_token)
folder_prefix = "Asii/"
user = g.get_user()
repo = user.create_repo(GITHUB_REPO)

# repo_path = "C:/TFS/tfs-migration12"
# repo = git.Repo(repo_path)

# repo.git.execute(["git", "lfs", "install"])

# repo.git.execute(["git", "lfs", "track", "*.exe"])

# # exe_file = "C:/TFS/tfs-migration12/x64.dll"

# repo.git.add(".")

# commit_message = "Add exe file to Git LFS"
# repo.git.commit("-m", commit_message)

# repo.git.execute(["git", "push", "origin", "master"])

# print("Successfully pushed")


import os

# Define the path to the project directory
project_dir = "C:/TFS/tfs-migration12"

# Change to the directory of the project
os.chdir(project_dir)

# Initialize Git LFS for the project
os.system("git lfs install")

# Loop through all subdirectories in the project directory
for dirpath, dirnames, filenames in os.walk("."):
    # Change to the subdirectory
    os.chdir(dirpath)

    # Track all executable files in the subdirectory and its subdirectories
    os.system("git lfs track '*.exe'")

    # Add all files in the subdirectory and its subdirectories to Git
    os.system("git add .")

    # Commit the changes with a message indicating the subdirectory name
    os.system(f"git commit -m 'Upload {os.path.basename(dirpath)} to Git'")

    # Return to the project directory
    os.chdir(project_dir)

# Push the changes to the remote repository
os.system("git push origin master")

