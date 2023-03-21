import subprocess
import winrm
from credentials import cred, server, path,projects
import os

user = cred.get('USER')
password = cred.get('PASSWORD')
url = server.get('host')
defpath = path.get('repos')
name = "dprog-demo"

sess = winrm.Session(url, auth=(user, password), transport='ntlm')

# Set the directory containing the Git repository
repo_dir = defpath + name

# Navigate to the repository directory in PowerShell
powershell_cd_cmd = f"cd {repo_dir}"
x= sess.run_ps("Set-Location "+defpath)
# subprocess.run(["powershell", "-Command", powershell_cd_cmd], check=True)

# Initialize a new Git repository
a = sess.run_ps("git init")

# Add files to the repository
b = sess.run_ps("git add .")

# Commit changes to the repository
commit_msg = "Initial commit"
c = sess.run_ps("git commit -m " +commit_msg)

# # Push changes to a remote repository
# remote_name = "origin"
# branch_name = "main"
# subprocess.run(["git", "push", remote_name, branch_name], check=True)

def add_git_repo():
    
    os.system('git init')
    os.system('git add .')
    commit_message = "Initial commit"
    os.system(f'git commit -m "{commit_message}"')
    remote_url = "https://github.com/<username>/<repository>.git"
    os.system(f'git remote add origin {remote_url}')
    os.system('git push -u origin main')