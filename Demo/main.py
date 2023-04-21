"""
  Main Execution code
"""
import os
import shutil
import subprocess
import library
from credentials import cred, server, path, server_urls, projects

user = cred.get('USER')
csv_file_path = path.get('csv_file')
password = cred.get('PASSWORD')
url = server.get('host')
git_user = cred.get('owner')
git_pwd = cred.get('token')
server_url = server_urls.get('http_url')
projects_with_path = library.get_list_of_branches()

def migration(project, path, output_file):
    """source code migration"""
    branch_name = path.split('/')[-1]
    defpath = os.path.join("C:\\", "Demo", project, branch_name)

    cmd1 = f'git tfs clone "{server_url}DefaultCollection" {path} "{defpath}" --username "{user}" --password "{password}"'
    cmd2 = 'git remote remove origin'
    cmd3 = f'git remote add origin https://{git_user}:{git_pwd}@github.com/{git_user}/{project}.git'
    cmd4 = f'git checkout -b {branch_name}'
    cmd5 = f'git push -u origin {branch_name}'

    try:
        subprocess.run(cmd1, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error cloning TFS repository: {e}")
        return
    library.list_files(defpath, output_file)
    os.chdir(defpath)
    try:
        subprocess.run(cmd2, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error removing origin remote: {e}")
    try:
        subprocess.run(cmd3, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error adding GitHub remote: {e}")
        return
    try:
        subprocess.run(cmd4, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error creating branch: {e}")
        return
    try:
        subprocess.run(cmd5, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error pushing branch to GitHub: {e}")
        return

    library.upload_binary_to_git_lfs(defpath, csv_file_path, branch_name)
    shutil.rmtree(defpath, ignore_errors=True)
for project, paths in projects_with_path.items():
    if project == projects.get('project5'):
        library.create_repo(project)
        output_file = "Source_repo_info"
        for path in paths:
            print(f"Migration for {path}")
            migration(project, path, output_file)

library.clone_target_git()
