import winrm
from credentials import cred, server, path

user = cred.get('USER')
password = cred.get('PASSWORD')
url = server.get('host')
defpath = path.get('repos')
path = defpath.strip()

sess = winrm.Session(url, auth=(user, password), transport='ntlm')
cd1 = sess.run_ps("Set-Location "+defpath)
result = sess.run_ps("Get-ChildItem -Directory "+defpath +"| select Name")
directories = result.std_out.splitlines()
for directory in directories[3:]:
    if len(directory) >0:
        dir_path = directory.decode('utf-8')
        print(dir_path)
        print("------------")
    cd2 = sess.run_ps("Set-Location "+defpath+dir_path)
    result2 = sess.run_ps("Get-ChildItem "+defpath+dir_path+"| select Name")
    #print(result2,"result2")
    directories2 = result2.std_out.splitlines()
    # print(directories2)

    if len(directory) >0:
        for directory1 in directories2[3:]:
            if len(directory1) >0:
                dir_name = directory1.decode('utf-8')
                print(dir_name)
            if("Binary" in dir_name or "Build" in dir_name):
                    cd3 = sess.run_ps("Set-Location "+defpath+dir_path+"/"+dir_name)
                    result3 = sess.run_ps("Get-ChildItem "+defpath+dir_path+"/"+dir_name+"| select Name")
                    directories3 = result3.std_out.splitlines()
                    if len(dir_name) >0:
                        count =0
                        for directorytemp in directories3[3:]:
                            tempDirectory=directorytemp.decode('utf-8')
                            print(tempDirectory)
                            if len(tempDirectory)>0:
                                count=count+1
                    print(dir_name +"dir count=")
                    print(count)

        print()


