import git
from github import Github
import os
from credentials import cred, data, path


access_token = cred.get('token')
GITHUB_REPO = data.get('name')
g = Github(access_token)
folder_prefix = "Asii/"
user = g.get_user()
repo = user.create_repo(GITHUB_REPO, auto_init=True)

project_dir = path.get('loc_repo')

# Initialize a Git repository in the project directory
repo = git.Repo.init(project_dir)

remote_name = "origin"
remote_branch_name = "master"
remote_branch = repo.remote(remote_name).refs[remote_branch_name]
local_branch = repo.heads.master
local_branch.set_tracking_branch(remote_branch)

# Initialize Git LFS for the project
repo.git.lfs("install")

# Function to check if a file is a binary file
def is_binary_file(filepath):
    with open(filepath, 'rb') as f:
        for _ in range(10):  # Read 10 chunks of 1024 bytes each
            chunk = f.read(1024)
            if b'\0' in chunk:
                return True
    return False

# Get the list of extensions to track with Git LFS from the user
extensions = input("Enter a comma-separated list of file extensions to track with Git LFS: ")
extensions = extensions.split(",")

# Define the root directory for the project
root_dir = os.path.abspath(project_dir)

for root, dirs, files in os.walk(root_dir):
    # Exclude the .git directory
    if ".git" in dirs:
        dirs.remove(".git")
    # Add all files to Git and upload binary files to Git LFS
    for file in files:
        filepath = os.path.join(root, file)
        print(filepath)
        if os.path.splitext(filepath)[1] in extensions and is_binary_file(filepath):
            repo.git.lfs("track", filepath)
        repo.index.add([filepath])

# repo.index.commit("Upload project to Git")
repo.index.commit("Upload project to Git", skip_hooks=True)


# Get the name of the default branch from the repository object
default_branch = repo.active_branch.name

# Find the remote branch with the same name as the default branch
remote_branches = [b for b in repo.heads if b.name == default_branch]
if len(remote_branches) == 0:
    raise ValueError(f"No remote branch found with name '{default_branch}'")
remote_branch = remote_branches[0]

# Get the name of the remote branch that the local branch is tracking
tracking_branch = remote_branch.tracking_branch()
if tracking_branch is None:
    raise ValueError(f"No tracking branch found for local branch '{remote_branch.name}'")

# Get the remote repository object for the tracking branch
origin = repo.remote(name=tracking_branch.remote_name)

# Add a new remote that points to the repository you just created
repo.create_remote('origin', f"git@github.com:{user.login}/{GITHUB_REPO}.git")

# Push changes to the repository
repo.git.push('--set-upstream', 'origin', default_branch)


