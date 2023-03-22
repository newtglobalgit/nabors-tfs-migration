import os
import winrm
from credentials import cred, server, path, data, server_urls


user = cred.get('USER')
password = cred.get('PASSWORD')
url = server.get('host')
defpath = path.get('repos')
path = defpath.strip()
git_user = cred.get('owner')
git_pwd = cred.get('token')
server_url = server_urls.get('http_url')

project_dirs=["DPROG"]

sess = winrm.Session(url, auth=(user, password), transport='ntlm')

# tfs_path = '$/DPROG'
# git_path = 'C:\Migration'

defpath = "C:\Demo\\tfs"

cmd1 = 'git tfs clone '+server_url+'DefaultCollection $/dprog/infinity.net ' + defpath
cmd2 = 'git remote remove origin'
cmd3 = 'git remote add origin https://'+git_user+':'+git_pwd+'@github.com/'+git_user+'/tfs-migration.git'
cmd4 = 'git add -A'
cmd5 = 'git commit -m "migration"'
cmd6 = 'git push --all origin'

output1 = sess.run_ps(cmd1)
print(output1)
print(output1.std_out)
output2 = sess.run_ps("Set-Location "+defpath)
print(output2)
print(output2.std_err)
output3 = sess.run_ps(cmd2)
print(output3)
print(output3.std_out)
output3 = sess.run_ps("Set-Location "+defpath)
print(output3)
print(output3.std_out)
output4 = sess.run_ps(cmd3)
print(output4)
print(output4.std_out)
output5 = sess.run_ps(cmd4)
print(output5)
print(output5.std_out)
output6 = sess.run_ps(cmd6)
print(output6)
print(output6.std_out)



# import os
# import winrm

# # Define TFS and Git repository parameters
# user = 'tfs_user'
# password = 'tfs_password'
# tfs_url = 'http://tfs-server:8080/tfs/DefaultCollection'
# tfs_path = '$/DPROG'
# git_path = 'C:\Migration'


# # Create a WinRM session to run PowerShell commands
# sess = winrm.Session('tfs-server', auth=(user, password), transport='ntlm')

# # Clone the TFS repository to a local Git repository
# cmd = f'git tfs clone {tfs_url} {tfs_path} {git_path}'
# output = sess.run_ps(cmd)

# # Initialize the local Git repository
# os.chdir(git_path)
# os.system('git init')
# # os.system(f'git remote add {git_remote} {tfs_url}')


# # Print the output to the console
# print(output)