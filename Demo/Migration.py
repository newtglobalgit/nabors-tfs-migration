import os
import subprocess
import library
import warnings
import upload_github_actions
from credentials import cred, server, server_urls, projects

class Migration:
    def __init__(self):
        self.user = cred.get('USER')
        self.cwd = os.getcwd()
        self.csv_file_path = self.cwd + "\\extension.csv"
        self.regex_pattern_file_path = self.cwd + "\\regex_pattern.csv"
        self.password = cred.get('PASSWORD')
        self.url = server.get('host')
        self.git_user = cred.get('owner')
        self.git_pwd = cred.get('token')
        self.server_url = server_urls.get('http_url')
        self.projects_with_path = library.get_list_of_branches()
        self.flag = 'True'

    def run(self):
        warnings.filterwarnings("ignore")
        for project, paths in self.projects_with_path.items():
            warnings.filterwarnings("ignore")
            if project == projects.get('project4'):  ##change 5
                library.create_repo(project)
                output_file = "Source_repo_info"
                for path in paths:
                    print(f"Migration for {path}")
                    self.migrate(project, path, output_file)
        library.clone_target_git()

    def migrate(self, project, path, output_file):
        warnings.filterwarnings("ignore")
        global flag
        branch_name = path.split('/')[-1]
        defpath = os.path.join("C:\\", "Demo", project, branch_name)
        cmd1 = f'git tfs clone "{self.server_url}DefaultCollection" {path} "{defpath}" --username "{self.user}" --password "{self.password}"'
        cmd3 = f'git remote add origin https://{self.git_user}:{self.git_pwd}@github.com/{self.git_user}/{project}.git'
        cmd4 = f'git checkout -b {branch_name}'
        cmd5 = f'git push -u origin {branch_name}'
        try:
            a=subprocess.run(cmd1, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error cloning TFS repository: {e}")
            return
        if self.flag == 'True':
            library.source_list_of_files(defpath, output_file)
            self.flag = 'False'
        upload_github_actions.upload_github_actions(defpath)
        os.chdir(defpath)
        try:
            subprocess.run(cmd3, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error adding GitHub remote: {e}")
            return
        try:
            subprocess.run(cmd4, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error creating branch: {e}")
            return
        try:
            subprocess.run(cmd5, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error pushing branch to GitHub: {e}")
            return
        upload_github_actions.git_push(defpath, branch_name)
        library.upload_binary_to_git_lfs(defpath, self.csv_file_path, branch_name)
        library.upload_regex_binary_to_git_lfs(defpath, self.regex_pattern_file_path, branch_name)
