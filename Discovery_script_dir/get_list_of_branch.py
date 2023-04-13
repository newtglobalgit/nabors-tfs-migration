import winrm
from credentials import cred, server, server_urls, projects
import re

user = cred.get('USER')
password = cred.get('PASSWORD')
server_url = server_urls.get('http_url')
url = server.get('host')

sess = winrm.Session(url, auth=(user, password), transport='ntlm')

tfs_url = server_url + "DefaultCollection"

project = projects.get('project5')


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


# def get_list_of_branches(tfs_url):
#     command = "git tfs list-remote-branches " + tfs_url
#     try:
#         result = sess.run_cmd(command)
#         if result is None:
#             return set()
#         output = result.std_out.decode('utf-8')
#         paths = re.findall(r'\s+(\$\/\S+)', output)
#         paths = [p.lstrip('$/') for p in paths]  # Trim $/ from beginning of each path
#         paths = [p for p in paths if project in p]  # Only include paths that contain project
#         with open('output.txt', 'w') as f:
#             for path in paths:
#                 f.write(path + '\n')
#         return paths
#     except Exception as e:
#         raise Exception(f"Error occurred while executing command: {command}. Error message: {e}")



# trmp =get_list_of_branches(tfs_url)
# print(trmp)

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