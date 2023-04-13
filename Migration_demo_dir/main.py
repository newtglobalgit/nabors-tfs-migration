import os, shutil, subprocess, library, warnings, upload_github_actions
from credentials import cred, server, path, server_urls, projects

user = cred.get('USER')
cwd = os.getcwd()
csv_file_path = cwd + "\\extension.csv"
regex_pattern_file_path = cwd + "\\regex_pattern.csv"
password = cred.get('PASSWORD')
url = server.get('host')
git_user = cred.get('owner')
git_pwd = cred.get('token')
server_url = server_urls.get('http_url')
projects_with_path = library.get_list_of_branches()
flag = 'True'

def migration(project, path, output_file):
    warnings.filterwarnings("ignore")
    global flag
    branch_name = path.split('/')[-1]
    defpath = os.path.join("C:\\", "Demo", project, branch_name)

    cmd1 = f'git tfs clone "{server_url}DefaultCollection" {path} "{defpath}" --username "{user}" --password "{password}"'
    # cmd2 = 'git remote remove origin'
    cmd3 = f'git remote add origin https://{git_user}:{git_pwd}@github.com/{git_user}/{project}.git'
    cmd4 = f'git checkout -b {branch_name}'
    cmd5 = f'git push -u origin {branch_name}'

    try:
        a=subprocess.run(cmd1, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error cloning TFS repository: {e}")
        return
    if flag == 'True':
        library.source_list_of_files(defpath, output_file)
        flag = 'False'
    
    upload_github_actions.upload_github_actions(defpath)

    os.chdir(defpath)
    # try:
    #     subprocess.run(cmd2, shell=True, check=True)
    # except subprocess.CalledProcessError as e:
        # print(f"Error removing origin remote: {e}")
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
    upload_github_actions.git_push(defpath, branch_name)
    
    library.upload_binary_to_git_lfs(defpath, csv_file_path, branch_name)
    library.upload_regex_binary_to_git_lfs(defpath, regex_pattern_file_path, branch_name)
    # shutil.rmtree(defpath, ignore_errors=True)

for project, paths in projects_with_path.items():
    warnings.filterwarnings("ignore")
    if project == projects.get('project5'):
        library.create_repo(project)
        output_file = "Source_repo_info"
        for path in paths:
            print(f"Migration for {path}")
            migration(project, path, output_file)

library.clone_target_git()