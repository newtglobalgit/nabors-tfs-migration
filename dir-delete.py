import os
import winrm
from credentials import cred, server, path


user = cred.get('USER')
password = cred.get('PASSWORD')

sess = winrm.Session("192.168.3.197", auth=(user, password), transport='ntlm')
result = sess.run_ps("Remove-Item -Path C:/Demo/tfs -Recurse -Force")
#result = sess.run_ps("Get-ChildItem -Path 'C:\Demo\\tfs-migration'")
