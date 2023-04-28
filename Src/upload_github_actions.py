import os, shutil, subprocess

def upload_github_actions(repo_path):
    yaml_path = "C:/Users/jayakarthi/git/throughput/main.yml"
    git_dir = os.path.join(repo_path, ".github", "workflows")
    os.makedirs(git_dir, exist_ok=True)
    shutil.copy2(yaml_path, git_dir)

def git_push(repo_path, branch_name):
    h = subprocess.run(['git', 'add', '.'], cwd=repo_path)
    f = subprocess.run(['git', 'commit', '-m', f'Add YAML file to .github folder'], cwd=repo_path)
    e = subprocess.run(['git', 'push','-u','origin', f'{branch_name}'], cwd=repo_path)