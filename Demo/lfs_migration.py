import csv
import os
import list_files
import subprocess


def upload_binary_to_git_lfs(directory_path, extensions_file_path, branch_name):

    extensions= getting_binary_extensions(directory_path)

    with open(extensions_file_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            extensions.append(row[0])

    # list_files.find_files_with_extension(directory_path, extensions)

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

def getting_binary_extensions(defpath):
    binary_extensions = []
    for root, dirs, files in os.walk(defpath):
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
