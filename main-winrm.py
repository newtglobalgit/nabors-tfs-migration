import os
import winrm
from credentials import cred, server, path


user = cred.get('USER')
password = cred.get('PASSWORD')
url = server.get('host')
defpath = path.get('repos')
path = defpath.strip()


sess = winrm.Session(url, auth=(user, password), transport='ntlm')

print(sess)

def get_directory(path):
    cd1 = sess.run_ps("Set-Location "+defpath)
    result = sess.run_ps("Get-ChildItem -Directory "+defpath +"| select Name")
    directories = result.std_out.splitlines()
    for directory in directories[3:]:
        if len(directory) >0:
            dir_path = directory.decode('utf-8')
            write_dir_name_to_file(dir_path)
            write_dir_name_to_file("------------")
            child_dir=defpath+dir_path
            cd2 = sess.run_ps("Set-Location "+defpath+dir_path)
            result2 = sess.run_ps("Get-ChildItem "+child_dir+"| Select-Object Name,PSIsContainer")
            directories2 = result2.std_out.splitlines()
            
            if len(directory) >0:
                for directory1 in directories2[3:]:
                    
                    if len(directory1) >0:
                        dir_name = directory1.decode('utf-8')
                    
                        if "True" in dir_name:
                            dir_name_new = dir_name.split("True")
                            sub_dir_path = child_dir+"/"+dir_name_new[0]
                            write_dir_name_to_file("dir "+dir_name_new[0])
                            get_directory_data(sub_dir_path)
                            # get_Count(sub_dir_path)
                            write_dir_name_to_file("*---------*")

                        else :
                            dir_name_new = dir_name.split("False")
                            write_file_name_to_file(dir_name_new[0])
                #             get_Count(child_dir)
                # get_Count(child_dir)
                # write_to_file("")


# def get_Count(path):
#     cd_count = sess.run_ps("Set-Location "+path)
#     result_count = sess.run_ps("Get-ChildItem "+path+"| Where-Object {$_.Extension -eq '.exe' -or $_.Extension -eq '.dll' -or $_.Extension -eq '.bin'} | Select-Object Name,PSIsContainer")
#     directories_count = result_count.std_out.splitlines()
#     count =0
#     for directory_count in directories_count[3:]:
#         if len(directory_count) >0:
#             sampleDirectory = directory_count.decode('utf-8')
#             if len(sampleDirectory)>0:
#                 count=count+1
#     write_to_file("Binary count=" +str(count))
#     write_to_file("")


def get_directory_data(path):
    c_d = sess.run_ps("Set-Location " + path)
    dir_name = sess.run_ps("Get-ChildItem " + path + "| Select-Object Name,PSIsContainer")
    dir_group = dir_name.std_out.splitlines()
    for each_dir in dir_group[3:]:
        if len(each_dir) > 0:
            each_dir_name = each_dir.decode('utf-8')
            if "True" in each_dir_name:
                each_dir_name_parts = each_dir_name.split("True")
                sub_directory_path = path + "/" + each_dir_name_parts[0]
                write_dir_name_to_file("Directory:"+each_dir_name_parts[0])
                get_directory_data(sub_directory_path)
                write_dir_name_to_file("*---------*")
            else:
                each_dir_name_parts = each_dir_name.split("False")
                write_file_name_to_file(each_dir_name_parts[0])

# def get_Count(path):
#     cd_count = sess.run_ps("Set-Location "+path)
#     result_count = sess.run_ps("Get-ChildItem "+path+"| Where-Object {$_.Extension -eq '.exe' -or $_.Extension -eq '.dll' -or $_.Extension -eq '.bin'} | Select-Object Name,PSIsContainer")
#     directories_count = result_count.std_out.splitlines()
#     count_dict = {}
#     for directory_count in directories_count[3:]:
#         if len(directory_count) >0:
#             sampleDirectory = directory_count.decode('utf-8')
#             if len(sampleDirectory)>0:
#                 ext = os.path.splitext(sampleDirectory)[1]
#                 if ext in count_dict:
#                     count_dict[ext] += 1
#                 else:
#                     count_dict[ext] = 1
#     for ext, count in count_dict.items():
#         write_to_file(f"{ext} count = {count}")
#     write_to_file("")

# def get_Count(path):
#     cd_count = sess.run_ps("Set-Location "+path)
#     counts = {}
#     extensions = [".exe", ".dll", ".bin",".txt",".cs"]
#     for ext in extensions:
#         result_count = sess.run_ps("Get-ChildItem "+path+" -Recurse | Where-Object {$_.Extension -eq '"+ext+"'}")
#         directories_count = result_count.std_out.splitlines()
#         count = 0
#         for directory_count in directories_count[3:]:
#             if len(directory_count) > 0:
#                 count += 1
#         counts[ext] = count
#     for ext, count in counts.items():
#         write_to_file(f"{ext} count = {count}")
#     write_to_file("")


def write_dir_name_to_file(string):
    with open("output_dir.txt", "a") as file:
        file.write(string + "\n")
    
def write_file_name_to_file(string):
    with open("output_file.txt", "a") as file:
        file.write(string + "\n")

get_directory(path)