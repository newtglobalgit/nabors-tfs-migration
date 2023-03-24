import os
import winrm
import get_list_of_branch
import repo_github
from credentials import cred, server, path, server_urls

user = cred.get('USER')
password = cred.get('PASSWORD')
url = server.get('host')
git_user = cred.get('owner')
git_pwd = cred.get('token')
server_url = server_urls.get('http_url')
projects_with_path = get_list_of_branch.get_list_of_branches()

def migration(project, path):
    sess = winrm.Session(url, auth=(user, password), transport='ntlm')
    branch_name = path.split('/')[-1]
    defpath = "C:/Demo/" + project
    ps_cmd = f'Set-Location "{defpath}"'
    cmd1 = f'git tfs clone "{server_url}DefaultCollection" {path} "{defpath}"'
    cmd2 = 'git remote remove origin'
    cmd3 = f'git remote add origin https://{git_user}:{git_pwd}@github.com/{git_user}/{project}.git'
    cmd4 = f'git checkout -b {branch_name}'
    cmd5 = f'git push -u origin {branch_name}'

    sess.run_ps(cmd1)
    sess.run_ps(ps_cmd + ';' + cmd2)
    sess.run_ps(ps_cmd + ';' + cmd3)
    sess.run_ps(ps_cmd + ';' + cmd4)
    sess.run_ps(ps_cmd + ';' + cmd5)
    
for project, paths in projects_with_path.items():
    repo_github.create_repo(project)
    for path in paths:
        print(f"Migration for {path}")
        migration(project, path)