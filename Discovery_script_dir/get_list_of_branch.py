import winrm , subprocess
from credentials import cred, server, server_urls, projects
import re , os
import pandas as pd

user = cred.get('USER')
password = cred.get('PASSWORD')
server_url = server_urls.get('http_url')
url = server.get('host')

sess = winrm.Session(url, auth=(user, password), transport='ntlm')

tfs_url = server_url + "/DefaultCollection"

project = projects.get('project5')


def migration(project_name, defpath):

    if os.path.exists(defpath):
        command = 'Remove-Item -Path {} -Recurse -Force'.format(defpath)
        p = subprocess.Popen(["powershell", "-Command",command]) 
        p.communicate()

    project_path = "$/"+project_name
    cmd1 = f'git tfs clone "{tfs_url}" {project_path} "{defpath}" --username "{user}" --password "{password}"'
    try:
        a=subprocess.run(cmd1, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error cloning TFS repository: {e}")
        return


def get_list_of_branches_path(tfs_url):
    command = "git tfs list-remote-branches " + tfs_url 
    try:
        result = sess.run_cmd(command)
        if result is None:
            return set()
        output = result.std_out.decode('utf-8')
        paths = re.findall(r'\s+(\$\/\S+)', output)
        paths = [p.lstrip('$/') for p in paths]  # Trim $/ from beginning of each path
        paths = [p for p in paths if project in p]  # Only include paths that contain project
        return paths
    except Exception as e:
        raise Exception(f"Error occurred while executing command: {command}. Error message: {e}")


# def get_branches_and_folders():

#     # Run tf.exe command to get the folder structure
#     tf_exe_path = r'& "C:\\Program Files\\Microsoft Visual Studio\\2022\\Community\\Common7\\IDE\\CommonExtensions\\Microsoft\\TeamFoundation\\Team Explorer\\TF.exe" dir "$/CatCore" /server:http://192.168.3.197:8080/tfs/DefaultCollection /login:Administrator,Obvious2023'

#     result = sess.run_ps(tf_exe_path)

#     # Print the output
#     output = result.std_out.decode('utf-8')
#     output_list = [line.strip() for line in output.split("\n") if '$' in line and '$/' not in line]

#     return output_list

def get_branches_and_folders():

    tf_exe_path = r'& "C:\\Program Files\\Microsoft Visual Studio\\2022\\Community\\Common7\\IDE\\CommonExtensions\\Microsoft\\TeamFoundation\\Team Explorer\\TF.exe" dir "$/CatCore" /server:http://192.168.3.197:8080/tfs/DefaultCollection /login:Administrator,Obvious2023'

    result = sess.run_ps(tf_exe_path)

    # Print the output
    output = result.std_out.decode('utf-8')
    output_list = [line.strip().replace('$', '') for line in output.split("\n") if '$' in line and '$/' not in line]

    return output_list


def get_list_of_branches(tfs_url):
    command = "git tfs list-remote-branches " + tfs_url
    try:
        result = sess.run_cmd(command)
        if result is None:
            return set()
        output = result.std_out.decode('utf-8')
        paths = re.findall(r'\s+(\$\/\S+)', output)
        paths = [p for p in paths if project in p] 
        return paths
    except Exception as e:
        raise Exception(f"Error occurred while executing command: {command}. Error message: {e}")
    



def get_file_structure():
    

    tf_exe_path = r'& "C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\IDE\CommonExtensions\Microsoft\TeamFoundation\Team Explorer\TF.exe" dir "$/CatCore" /files /recursive /server:http://192.168.3.197:8080/tfs/DefaultCollection /login:Administrator,Obvious2023 > C://Git//dir.txt'

    result = sess.run_ps(tf_exe_path)

    read_file_cmd = r'Get-Content C:\Git\dir.txt'
    read_file_result = sess.run_ps(read_file_cmd)
    output = read_file_result.std_out.decode('utf-8')

    num_files = output.count('\n') - 4 

    write_file_path = "C://Git//output.txt"
    with open(write_file_path, "w") as f:
        f.write(output)
        f.write(f"\n\nNumber of files: {num_files}")


# migration("CatCore", "C:\Discovery\CatCore")
get_branches_and_folders()