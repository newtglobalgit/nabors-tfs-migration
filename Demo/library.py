"""
  Library with set of methods
"""
import os
import re
import subprocess
import csv
import winrm
import collections
from github import Github
from credentials import cred, path, server, server_urls

access_token = cred.get('token')
user = cred.get('USER')
password = cred.get('PASSWORD')
server_url = server_urls.get('http_url')
url = server.get('host')
tfs_url = server_url+"DefaultCollection"
sess = winrm.Session(url, auth=(user, password), transport='ntlm')
file_types = collections.defaultdict(list)

def create_repo(GITHUB_REPO):
    """Create repo"""
    g = Github(access_token)
    user = g.get_user()
    user.create_repo(GITHUB_REPO)
    print(f"Repository '{GITHUB_REPO}' has been created.")

def get_list_of_branches():
    """get list of the tfs repo branches"""
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
    list(projects.keys())
    return projects

def list_files(directory, output_file):
    """Listing files"""
    file_count = 0
    folder_count = 0
    total_size = 0
    with open(output_file, 'w') as f:
        for root, dirs, files in os.walk(directory):
            file_count += len(files)
            folder_count += len(dirs)
            for file in files:
                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path)
                total_size += file_size
        f.write(f"Total folders: {folder_count}\n")
        f.write(f"Total files: {file_count}\n")
        f.write(f"Total size: {total_size} bytes\n")

def getting_binary_extensions(defpath):
    """Binary extensions classifier"""
    binary_extensions = []
    for root, files in os.walk(defpath):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'rb') as f:
                try:
                    is_binary = b'\0' in f.read(512)
                except UnicodeDecodeError:
                    is_binary = True
                if is_binary:
                    extension = os.path.splitext(file_path)[1]
                    if extension not in binary_extensions:
                        binary_extensions.append(extension)
    return [ext for ext in binary_extensions if ext.startswith('.')]

def upload_binary_to_git_lfs(directory_path, extensions_file_path, branch_name):
    """Binary uploaded to git large file storage in GITHUB"""
    extensions= getting_binary_extensions(directory_path)
    with open(extensions_file_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            extensions.append(row[0])
    subprocess.run(['git', 'stash', 'save', 'Stashing changes'], cwd=directory_path)
    subprocess.run(['git', 'checkout', branch_name], cwd=directory_path)
    for root, files in os.walk(directory_path):
        for file in files:
            file_ext = os.path.splitext(file)[1].lower()
            if file_ext in extensions:
                try:
                    subprocess.run(['git', 'lfs', 'install'], cwd=root)
                    subprocess.run(['git', 'lfs', 'migrate', 'import', '--include', file, '--yes'], cwd=root)
                    subprocess.run(['git', 'lfs', 'track', file], cwd=root)
                    e = subprocess.run(['git', 'add', file], cwd=root)
                    f = subprocess.run(['git', 'commit', '-m', f'Moving {file} to Git LFS'], cwd=root)
                except subprocess.CalledProcessError as e:
                    print(f"Error occurred: {e.stderr}")
    subprocess.run(['git', 'push'], cwd=directory_path)

def file_with_extension(directory):
    """files with extension"""
    file_name = 'C://Users//ujjawalg//source//repos//demo-tfs//Reports.txt'
    try:
        with open(file_name, 'w') as f:
            for files in os.walk(directory):
                # Skip .git folders
                for file in files:
                    file_extension = os.path.splitext(file)[-1].lower()
                    if file_extension not in ('.gitignore', '.git'):
                        file_types[file_extension].append(file)
            for file_type, files in file_types.items():
                if file_type == '':
                    f.write("Files without extension: \n")
                    for file in files:
                        if file not in ('.gitignore', '.git', 'HEAD', 'cleanup'):
                            f.write(file + "\n")
    except Exception as e:
        print("An error occurred:", str(e))

def clone_target_git():
    """clone the github repository"""
    repo_url = path.get('git_repo')
    clone_directory = path.get('git_repo_path')
    output_file_name = 'C://Users//ujjawalg//source//repos//demo-tfs//Target_repo_info.txt'
    subprocess.run(["git", "clone", repo_url, clone_directory])
    file_with_extension(clone_directory)
    list_files(clone_directory, output_file_name)
