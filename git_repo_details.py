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

defpath = "C:\Demo\\tfs"

cmd1 = 'git tfs clone '+server_url+'DefaultCollection $/dprog/infinity.net ' + defpath

output1 = sess.run_ps(cmd1)

file_name = set()



def get_directory_data(path):
    c_d = sess.run_ps("Set-Location " + path)
    dir_name = sess.run_ps("Get-ChildItem " + path + "| Select-Object Name,PSIsContainer")
    dir_group = dir_name.std_out.splitlines()
    for each_dir in dir_group[3:]:
        if len(each_dir) > 0:
            each_dir_name = each_dir.decode('utf-8')
            if "True" in each_dir_name:
                each_dir_name_parts = each_dir_name.split(" ")
                sub_directory_path = path + "\\" + each_dir_name_parts[0]
                # write_dir_name_to_file("Directory:"+each_dir_name_parts[0])
                get_directory_data(sub_directory_path)
                # write_dir_name_to_file("*---------*")
            else:
                each_file_name_parts = each_dir_name.split(" ")
                sub_file_path = path + "\\" + each_file_name_parts[0]
                # write_file_name_to_file(each_dir_name_parts[0])
                file_name.add(each_file_name_parts[0])


get_directory_data(defpath)


# dictionary to store the filenames with each extension
extension_files = {}

extension_counts = {}

# list to store the files without any extension
no_extension_files = []


for line in file_name:
    extension = os.path.splitext(line.strip())[1]
    if extension:
        if extension in extension_files:
            extension_files[extension].append(line.strip())
            extension_counts[extension] += 1
        else:
            extension_files[extension] = [line.strip()]
            extension_counts[extension] = 1
    else:
        no_extension_files.append(line.strip())


output_file = input("Enter the output file name: ")
with open(output_file, "w") as file:
    file.write("Files grouped by extension:\n")
    for extension, files in extension_files.items():
        file.write(f"{extension}:\n")
        for f in files:
            file.write(f"\t{f}\n")
   
    file.write("Extension counts:\n")
    for extension, count in extension_counts.items():
        file.write(f"\t{extension}: {count}\n")

    if no_extension_files:
        file.write("Files Ignored:\n")
        for f in no_extension_files:
            file.write(f"\t{f}\n")

