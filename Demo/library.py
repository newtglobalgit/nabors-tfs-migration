import os, re, csv, winrm, subprocess
from github import Github
from credentials import cred, path, server, server_urls

access_token = cred.get('token')
user = cred.get('USER')
password = cred.get('PASSWORD')
server_url = server_urls.get('http_url')
url = server.get('host')
tfs_url = server_url+"DefaultCollection"
sess = winrm.Session(url, auth=(user, password), transport='ntlm')

def create_repo(GITHUB_REPO):
    g = Github(access_token)
    user = g.get_user()
    repo = user.create_repo(GITHUB_REPO)
    print(f"Repository '{GITHUB_REPO}' has been created.")

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
    list(projects.keys())
    return projects

def list_files(directory, output_file):
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
    extensions= getting_binary_extensions(directory_path)
    with open(extensions_file_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            extensions.append(row[0])
    subprocess.run(['git', 'stash', 'save', 'Stashing changes'], cwd=directory_path)
    b = subprocess.run(['git', 'checkout', branch_name], cwd=directory_path)
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_ext = os.path.splitext(file)[1].lower()
            if file_ext in extensions:
                try:
                    h = subprocess.run(['git', 'lfs', 'install'], cwd=root)
                    d = subprocess.run(['git', 'lfs', 'migrate', 'import', '--include', file, '--yes'], cwd=root)
                    g = subprocess.run(['git', 'lfs', 'track', file], cwd=root)
                    e = subprocess.run(['git', 'add', file], cwd=root)
                    f = subprocess.run(['git', 'commit', '-m', f'Moving {file} to Git LFS'], cwd=root)
                except subprocess.CalledProcessError as e:
                    print(f"Error occurred: {e.stderr}")
    c = subprocess.run(['git', 'push'], cwd=directory_path)