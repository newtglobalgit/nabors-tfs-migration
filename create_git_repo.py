import subprocess
import winrm
from credentials import cred, server, path,projects

user = cred.get('USER')
password = cred.get('PASSWORD')
url = server.get('host')
defpath = path.get('repos')
name = projects.get('project1')

sess = winrm.Session(url, auth=(user, password), transport='ntlm')

# Set the directory containing the Git repository
repo_dir = defpath + name

# Navigate to the repository directory in PowerShell
powershell_cd_cmd = f"cd {repo_dir}"
sess.run_ps("Set-Location "+defpath)
# subprocess.run(["powershell", "-Command", powershell_cd_cmd], check=True)

# Initialize a new Git repository
subprocess.run(["git", "init"], check=True)

# Add files to the repository
subprocess.run(["git", "add", "."], check=True)

# Commit changes to the repository
commit_msg = "Initial commit"
subprocess.run(["git", "commit", "-m", commit_msg], check=True)

# # Push changes to a remote repository
# remote_name = "origin"
# branch_name = "main"
# subprocess.run(["git", "push", remote_name, branch_name], check=True)