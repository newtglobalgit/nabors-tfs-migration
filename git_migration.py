import os
import winrm
import get_list_of_branch
# import git_repo_details
import repo_github
import moving_binary_ascii_to_git_lfs
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

    # git_repo_details.get_directory_data(defpath)

    sess.run_ps(ps_cmd + ';' + cmd2)
    sess.run_ps(ps_cmd + ';' + cmd3)
    sess.run_ps(ps_cmd + ';' + cmd4)
    sess.run_ps(ps_cmd + ';' + cmd5)
    moving_binary_ascii_to_git_lfs.moving_binary_ascii_to_git_lfs(defpath)
    

for project, paths in projects_with_path.items():
    repo_github.create_repo(project)
    for path in paths:
        print(f"Migration for {path}")
        migration(project, path)


# import os
# import winrm
# import get_list_of_branch
# # import git_repo_details
# import repo_github
# from credentials import cred, server, path, server_urls


# user = cred.get('USER')
# password = cred.get('PASSWORD')
# url = server.get('host')
# git_user = cred.get('owner')
# git_pwd = cred.get('token')
# server_url = server_urls.get('http_url')

# # Define the file extensions to be stored in Git LFS
# BINARY_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.mp4', '.pdf', '.doc', '.xls', '.ppt']
# ASCII_EXTENSIONS = ['.txt', '.py', '.c', '.cpp', '.h', '.hpp', '.md', '.html', '.css', '.js']

# projects_with_path = get_list_of_branch.get_list_of_branches()

# def migration(project, path):

#     sess = winrm.Session(url, auth=(user, password), transport='ntlm')

#     branch_name = path.split('/')[-1]

#     defpath = "C:/Demo/" + project
    
#     ps_cmd = f'Set-Location "{defpath}"'

#     cmd0 = 'git lfs install'

#     cmd1 = f'git tfs clone "{server_url}DefaultCollection" {path} "{defpath}"'

#     cmd2 = 'git remote remove origin'

#     cmd3 = f'git remote add origin https://{git_user}:{git_pwd}@github.com/{git_user}/{project}.git'

#     cmd4 = f'git checkout -b {branch_name}'

#     cmd5 = f'git lfs migrate import --include="*.{",".join(BINARY_EXTENSIONS)}"'

#     cmd6 = 'git add .'

#     cmd7 = 'git commit -m "Adding binary files to Git LFS"'

#     cmd8 = f'git push -u origin {branch_name}'

#     sess.run_ps(cmd0)

#     sess.run_ps(cmd1)

#     # git_repo_details.get_directory_data(defpath)

#     sess.run_ps(ps_cmd + ';' + cmd2)
#     sess.run_ps(ps_cmd + ';' + cmd3)
#     sess.run_ps(ps_cmd + ';' + cmd4)
#     sess.run_ps(ps_cmd + ';' + cmd5)
#     sess.run_ps(ps_cmd + ';' + cmd6)
#     sess.run_ps(ps_cmd + ';' + cmd7)
#     sess.run_ps(ps_cmd + ';' + cmd8)

#     # Move ASCII files to Git LFS
#     for filename in os.listdir(defpath):
#         filepath = os.path.join(defpath, filename)
#         if os.path.isfile(filepath):
#             file_ext = os.path.splitext(filename)[1].lower()
#             if file_ext in ASCII_EXTENSIONS:
#                 cmd9 = f'git lfs migrate import --include="{filename}"'
#                 cmd10 = f'git add .'
#                 cmd11 = f'git commit -m "Moving {filename} to Git LFS"'
#                 sess.run_ps(ps_cmd + ';' + cmd9)
#                 sess.run_ps(ps_cmd + ';' + cmd10)
#                 sess.run_ps(ps_cmd + ';' + cmd11)
#     sess.run_ps(ps_cmd + '; git push')

# for project, paths in projects_with_path.items():
#     repo_github.create_repo(project)
#     for path in paths:
#         print(f"Migration for {path}")
#         migration(project, path)

