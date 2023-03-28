import winrm
from github import Github 
from credentials import cred, data 


def delete_repo_and_dir(GITHUB_REPO,path):
    access_token = cred.get('token') 
    # GITHUB_REPO = data.get('name')  
    g = Github(access_token) 
    target_repo = data.get('name') 
    repo = g.get_user().get_repo(target_repo) 
    repo.delete() 
    print("repo deleted")
    user = cred.get('USER')
    password = cred.get('PASSWORD')
    sess = winrm.Session("192.168.3.197", auth=(user, password), transport='ntlm')
    cmd = "Remove-Item -Path "+path+" -Recurse -Force"
    result = sess.run_ps(cmd)
#result = sess.run_ps("Get-ChildItem -Path 'C:\Demo\\tfs-migration'")