#!/usr/bin/env python
import winrm
from credentials import cred, server, path

user = cred.get('USER')
password = cred.get('PASSWORD')
url = server.get('host')
defpath = path.get('repos')
path = defpath.strip()

# Create winrm connection.
sess = winrm.Session(url, auth=(user, password), transport='ntlm')
cd1 = sess.run_ps("Set-Location "+ defpath)
result = sess.run_ps("Get-ChildItem -Directory "+ defpath + "| select Name")
print(result.std_out)
