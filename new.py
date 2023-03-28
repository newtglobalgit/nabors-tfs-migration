import os
import re
import subprocess
# from credentials import server_urls


directory_path = 'C:\Demo\dprog'
server_url = "http://192.168.3.197:8080/tfs/"
tfs_url = server_url+"DefaultCollection"


def upload_ascii_binary_to_git_lfs(directory_path, extensions,branch_name):
                
    subprocess.run(['git', 'stash','save','Stashing changes'], cwd=directory_path)
    b=subprocess.run(['git', 'checkout', branch_name],cwd=directory_path)
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_ext = os.path.splitext(file)[1].lower() 
            if file_ext in extensions:
                try:
                    h=subprocess.run(['git', 'lfs','install'], cwd=root)
                    d=subprocess.run(['git', 'lfs', 'migrate', 'import', '--include', file, '--yes'], cwd=root)
                    g=subprocess.run(['git', 'lfs','track', file], cwd=root)
                    e=subprocess.run(['git', 'add', file], cwd=root)
                    f=subprocess.run(['git', 'commit', '-m', f'Moving {file} to Git LFS'], cwd=root)
                    
                except subprocess.CalledProcessError as e:
                    print(f"Error occurred: {e.stderr}")

    c=subprocess.run(['git', 'push', ], cwd=directory_path)

def get_list_of_branches():
    extensions = input("Enter the extensions you want to migrate to Git LFS (separated by comma): ")
    extensions = [ext.strip().lower() for ext in extensions.split(",")]
    BINARY_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.mp4', '.pdf', '.doc', '.xls', '.ppt', '.exe', '.dll', '.bin']
    extensions += BINARY_EXTENSIONS

    
    command = "git tfs list-remote-branches " + tfs_url
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    
    output = result.stdout
    
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
    
    # if not os.path.exists(os.path.join(directory_path, '.git')):
    a= subprocess.run(['git', 'init'], cwd=directory_path)

    project_names = list(projects.keys())
    for project_name in project_names:
        paths = projects[project_name]
        for path in paths:
            print(f"Migration for {path}")
            branch_name = path.split('/')[-1]
            if not os.path.exists(os.path.join(directory_path, '.git')):
                a = subprocess.run(['git', 'init'], cwd=directory_path)

            upload_ascii_binary_to_git_lfs(directory_path, extensions, branch_name)

            


# Call the function to get the list of branches and upload files to Git LFS
get_list_of_branches()




