import winrm,  re
from credentials import cred, server, server_urls

user = cred.get('USER')
password = cred.get('PASSWORD')
server_url = server_urls.get('http_url')
url = server.get('host')
sess = winrm.Session(url, auth=(user, password), transport='ntlm')
tfs_url = server_url+"DefaultCollection"

def get_list_of_branches():
    command = "git tfs list-remote-branches " + tfs_url
    result = sess.run_cmd(command)
    output = result.std_out.decode('utf-8')
    paths = re.findall(r'\s+(\$\/\S+)', output)
    projects = {}

    for path in paths:
        match = re.match(r'\$/([^/]+)/', path)
        if match:
            project_name = match.group(1)
            if project_name in projects:
                projects[project_name].append(path)
            else:
                projects[project_name] = [path]

    project_names = list(projects.keys())
    return projects

get_list_of_branches()