import os, re, csv, winrm, subprocess, collections, warnings, hashlib
from github import Github
from credentials import cred, path, server, server_urls

access_token = cred.get('token')
organization_name = cred.get('org')
user = cred.get('USER')
password = cred.get('PASSWORD')
server_url = server_urls.get('http_url')
url = server.get('host')
tfs_url = server_url+"DefaultCollection"
sess = winrm.Session(url, auth=(user, password), transport='ntlm')
file_types = collections.defaultdict(list)
cwd = os.getcwd()
source_dir_hash = ''
source_file_count =0
source_folder_count =0
source_dir_total_size = 0
source_dir_list = []
target_dir_list = []

def delete_dir_and_repo(target_repo):
    access_token = cred.get('token')
    git_authorize = Github(access_token)
    repo = git_authorize.get_organization(organization_name).get_repo(target_repo)
    repo.delete()
    print("repo deleted")
    sess = winrm.Session("192.168.3.197", auth=(user, password), transport='ntlm')
    p = subprocess.Popen(["powershell.exe", "Remove-Item -Path C:/Demo -Recurse -Force"]) 
    p.communicate()


def create_repo(github_repo):
    warnings.filterwarnings("ignore")
    git_authorize = Github(access_token)
    user = git_authorize.get_organization(organization_name)
    repo_names = [repo.name for repo in git_authorize.get_organization(organization_name).get_repos()]
    if github_repo in repo_names:
        print(f"Repository '{github_repo}' already exists.")
        delete_dir_and_repo(github_repo)
        create_repo(github_repo)
        print(f"Existing Repository '{github_repo}' removed and new '{github_repo}' has been created.")
    else:
        user.create_repo(github_repo)
        print(f"Repository '{github_repo}' has been created.")

def get_file_checksum(file_path):
    with open(file_path, 'rb') as f:
        file_data = f.read()
        md5_checksum = hashlib.md5(file_data).hexdigest()
    return md5_checksum

def get_list_of_branches():
    warnings.filterwarnings("ignore")
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

def source_list_of_files(directory, output_file):
    warnings.filterwarnings("ignore")
    source_file_count = 0
    source_folder_count = 0
    source_dir_total_size = 0
    source_dir_list = []
    ignore = ['.git', '.gitignore','.gitattributes'] # Add ignore list here
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in ignore] # Exclude dirs in ignore list
        files[:] = [f for f in files if f not in ignore] # Exclude files in ignore list
        source_file_count += len(files)
        source_folder_count += len(dirs)
        for file in files:
            file_path = os.path.join(root, file)
            file_size = os.path.getsize(file_path)
            source_dir_total_size += file_size
            source_dir_list.append((file_path, file_size, get_file_checksum(file_path)))
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            source_dir_list.append((dir_path, 0, ""))
    with open(output_file, 'w') as f:
        warnings.filterwarnings("ignore")
        f.write(f"Number of folders: {source_folder_count}\n")
        f.write(f"Number of files: {source_file_count}\n")
        f.write(f"Total size: {source_dir_total_size / (1024*1024):.2f} MB\n")
        for root, dirs, files in os.walk(directory):
            if root in ignore: # Skip root if it's in ignore list
                continue
            level = root.replace(directory, '').count(os.sep)
            indent = ' ' * 4 * (level)
            f.write('{}{}/\n'.format(indent, os.path.basename(root)))
            subindent = ' ' * 4 * (level + 1)
            for file in files:
                if file in ignore: # Skip file if it's in ignore list
                    continue
                temp_file_path = os.path.join(root, file)
                temp_file_size = os.path.getsize(temp_file_path)
                temp_file_checksum = get_file_checksum(temp_file_path)
                f.write('{}{} ({}, {})\n'.format(subindent, file, temp_file_size, temp_file_checksum))

def getting_binary_extensions(defpath):
    warnings.filterwarnings("ignore")
    binary_extensions = []
    for root, dir, files in os.walk(defpath):
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

def upload_regex_binary_to_git_lfs(directory_path, regex_file_path, branch_name):
    warnings.simplefilter("ignore")
    regex_patterns = []
    with open(regex_file_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            regex_patterns.append(row[0])
    subprocess.run(['git', 'stash', 'save', 'Stashing changes'], cwd=directory_path)
    b = subprocess.run(['git', 'checkout', branch_name], cwd=directory_path)

    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_ext = os.path.splitext(file)[1].lower()
            file_size = os.path.getsize(file_path)
            for pattern in regex_patterns:
                if re.search(pattern, file) or file_size > 30 * 1024 * 1024:  # 30 MB in bytes
                    try:
                        h = subprocess.run(['git', 'lfs', 'install'], cwd=root)
                        d = subprocess.run(['git', 'lfs', 'migrate', 'import', '--include', file, '--yes'], cwd=root)
                        g = subprocess.run(['git', 'lfs', 'track', file], cwd=root)
                        e = subprocess.run(['git', 'add', file], cwd=root)
                        f = subprocess.run(['git', 'commit', '-m', f'Moving {file} to Git LFS'], cwd=root)
                    except subprocess.CalledProcessError as e:
                        print(f"Error occurred: {e.stderr}")
    c = subprocess.run(['git', 'push'], cwd=directory_path)

def upload_binary_to_git_lfs(directory_path, extensions_file_path, branch_name):
    warnings.simplefilter("ignore")
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

def file_with_extension(directory):
    warnings.filterwarnings("ignore")
    file_name = cwd+'//Reports.txt'
    try:
        with open(file_name, 'w') as f:
            for root, dirs, files in os.walk(directory):
                # Skip .git folders
                for file in files:
                    file_extension = os.path.splitext(file)[-1].lower()
                    if file_extension not in ('.gitignore', '.git'):
                        file_types[file_extension].append(file)
                        
            for file_type, files in file_types.items():
                if file_type == '':
                    f.write("Files without extension: \n")
                    for file in files:
                        if file not in ('.gitignore', '.git', 'HEAD', 'cleanup','5e5d0a65b4157d1a521e6e37272f7a33deae11b36fadcfb3be50888a9e7301d8'):
                            f.write(file + "\n")
    except Exception as e:
        print("An error occurred:", str(e))

def target_list_of_files(directory, output_file):
    warnings.filterwarnings("ignore")
    file_count = 0
    folder_count = 0
    total_size = 0
    target_dir_list = []
    ignore = ['.git', '.gitignore','.github','.gitattributes']
    with open(output_file, 'w') as f:
        for root, dirs, files in os.walk(directory):
            dirs[:] = [d for d in dirs if d not in ignore] 
            files[:] = [f for f in files if f not in ignore]
            file_count += len(files)
            folder_count += len(dirs)
            for file in files:
                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path)
                file_checksum = get_file_checksum(file_path)
                total_size += file_size
                target_dir_list.append((file_path, file_size, file_checksum))
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                target_dir_list.append((dir_path, 0, ""))
        f.write(f"Number of folders: {folder_count}\n\n")
        f.write(f"Files in Git LFS: \n")
    temp_count = 0
    output = subprocess.check_output(['git', 'lfs', 'ls-files', '--size'], cwd=directory)
    output = output.decode('utf-8')
    with open(output_file, 'a') as f:
        for line in output.splitlines():
            line_parts = line.split()
            if len(line_parts) >= 3:
                filename = ' '.join(line_parts[2:])
                f.write(f"{filename}\n")
                temp_count += 1
                file_size = line_parts[-2]
                file_type = line_parts[-1]
                file_size = float(file_size.split("(")[1])
                file_type = file_type.split(")")[0]
                if file_type == 'MB':
                    file_size = file_size * 1024 * 1024  # convert bytes to MB
                elif file_type == 'KB':
                    file_size = file_size * 1024  # convert KB to MB
                total_size+=file_size
        f.write(f"Git lfs file count: {temp_count} \n\n")
        f.write(f"Number of files including git-lfs: {file_count}\n\n")
        f.write(f"Total size: {total_size / (1024*1024):.2f} MB\n\n")
        f.write(f"List of files with their size and checksum: \n")
        for file_path, file_size, file_checksum in target_dir_list:
            f.write(f"{file_path} ({file_size}) {file_checksum}\n")

def clone_target_git():
    warnings.filterwarnings("ignore")
    repo_url = path.get('git_repo')
    clone_directory = path.get('git_repo_path')
    output_file_name = cwd+'//Target_repo_info.txt'
    subprocess.run(["git", "clone", "--recursive", repo_url, clone_directory])
    subprocess.run(["git","lfs","pull", clone_directory]) 
    file_with_extension(clone_directory)
    target_list_of_files(clone_directory, output_file_name)
    