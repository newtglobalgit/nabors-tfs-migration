import os
import git
from git import Repo
from git import GitCommandError
import subprocess

# Define the path to your project directory
PROJECT_PATH = '/path/to/your/project'

# Define the path to your Git repository
REPO_PATH = '/path/to/your/repository'

# Initialize a new Git repository
repo = git.Repo.init(REPO_PATH)

# Configure the repository to use Git LFS
lfs_path = os.path.join(REPO_PATH, '.git', 'lfs')
os.makedirs(lfs_path, exist_ok=True)
with open(os.path.join(lfs_path, 'config'), 'w') as f:
    f.write('[lfs]\n  url = https://github.com/git-lfs/git-lfs.git/info/lfs\n')

# Add the project files to the Git repository
repo.index.add([os.path.join(PROJECT_PATH, f) for f in os.listdir(PROJECT_PATH)])

# Commit the changes to the repository
try:
    repo.index.commit("Initial commit")
except GitCommandError as e:
    if 'no changes added to commit' not in e.stderr:
        raise e

# Push the changes to the remote repository
try:
    origin = repo.remote(name='origin')
    origin.push()
except GitCommandError as e:
    if 'git-lfs/2.12.0' in e.stderr:
        subprocess.run(['git', 'lfs', 'install'], cwd=REPO_PATH)
        origin.push()
    else:
        raise e

# Track the large files with Git LFS
subprocess.run(['git', 'lfs', 'track', os.path.join(PROJECT_PATH, '*')], cwd=REPO_PATH)

# Add the tracked files to the Git repository
repo.index.add([os.path.join(PROJECT_PATH, f) for f in os.listdir(PROJECT_PATH)])

# Commit the changes to the repository
try:
    repo.index.commit("Add large files with Git LFS")
except GitCommandError as e:
    if 'no changes added to commit' not in e.stderr:
        raise e

# Push the changes to the remote repository
try:
    origin = repo.remote(name='origin')
    origin.push()
except GitCommandError as e:
    if 'git-lfs/2.12.0' in e.stderr:
        subprocess.run(['git', 'lfs', 'install'], cwd=REPO_PATH)
        origin.push()
    else:
        raise e
