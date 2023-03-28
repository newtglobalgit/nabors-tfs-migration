import subprocess, git_dir_details
from credentials import path

repo_url = path.get('git_repo')
clone_directory = path.get('git_repo_path')
output_file = "Target_repo_info"
subprocess.run(["git", "clone", repo_url, clone_directory])
git_dir_details.list_files(clone_directory, output_file)