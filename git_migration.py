import os
import winrm
from credentials import cred, server, path, data, server_urls

user = cred.get('USER')
password = cred.get('PASSWORD')
url = server.get('host')
git_user = cred.get('owner')
git_pwd = cred.get('token')
server_url = server_urls.get('http_url')

project_dirs=["DPROG"]
defpath = "C:/Demo/tfs"

sess = winrm.Session(url, auth=(user, password), transport='ntlm')

# Set the current directory
ps_cmd = f'Set-Location "{defpath}"'

# Clone the git repository
cmd1 = f'git tfs clone "{server_url}DefaultCollection" $/Sample_Practice_Project/Main "{defpath}"'

# Remove the origin remote
cmd2 = 'git remote remove origin'

# Add the origin remote
cmd3 = f'git remote add origin https://{git_user}:{git_pwd}@github.com/{git_user}/tfs-migration.git'


cmd4 = 'git push --all origin'


output1 = sess.run_ps(cmd1)
output2 = sess.run_ps(ps_cmd + ';' + cmd2)
output3 = sess.run_ps(ps_cmd + ';' + cmd3)
output4 = sess.run_ps(ps_cmd + ';' + cmd4)




