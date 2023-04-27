from github import Github
import datetime, requests, time
import pandas as pd
from credentials import cred, path, server_urls, projects

github_token = cred.get('token')
repo_owner = cred.get('owner')
repo_name = projects.get('project5')
start_time = time.time()
today = datetime.date.today().strftime("%Y-%m-%d")

def get_commit_info(github_token, repo_owner, repo_name):
    g = Github(github_token)
    repo = g.get_repo(f"{repo_owner}/{repo_name}")
    commit_info_list = []
    for branch_idx, branch in enumerate(repo.get_branches()):
        branch_name = branch.name
        last_commit_date = None
        total_commit_count = 0
        last_author_name = None
        for commit in repo.get_commits(sha=branch.commit.sha):
            try:
                commit_id = commit.sha
                author_name = commit.author.name
                comment = commit.commit.message
            except AttributeError:
                comment = '<no comment>'
            date = commit.commit.author.date
            total_commit_count += 1
            if last_commit_date is None or date > last_commit_date:
                last_commit_date = date
                last_author_name = author_name
            if last_commit_date is not None:
                try:
                    last_commit_date = last_commit_date
                except AttributeError:
                    print(f"Warning: Invalid date format: {last_commit_date}")
            else:
                last_commit_date = '<no date>'
        branch_id = f"Branch{branch_idx+1}"
        Repo_Name = repo_name
        commit_info_list.append({'Repo Name': Repo_Name,'Branch Name': branch_name,'Branch ID': branch_id, 'Branch path': branch_name, 'Total commit count': total_commit_count, 'Last Commit Date': last_commit_date, 'Last Commit By': last_author_name})
    commit_df = pd.DataFrame(commit_info_list, columns=['Repo Name','Branch Name','Branch ID', 'Branch path', 'Total commit count', 'Last Commit Date', 'Last Commit By'])
    return commit_df

def get_file_structure_to_excel(access_token, repo_name, branch_name, user_name):
    g = Github(access_token)
    repo = g.get_repo(f'{user_name}/{repo_name}')
    file_structure = []
    contents = repo.get_contents("", ref=branch_name)
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            if file_content.name == ".git":
                continue
            contents.extend(repo.get_contents(file_content.path, ref=branch_name))
        else:
            if file_content.name in [".gitattributes", ".git", ".gitignore"]:
                continue
            extension = "." + file_content.name.split(".")[-1] if "." in file_content.name else ""
            directory = "/".join(file_content.path.split("/")[:-1]).replace("/", "\\")
            if not directory:
                directory_path = branch_name
            else:
                directory_path = branch_name + "\\" + directory
            size = file_content.size
            stored_in_lfs = False
            try:
                lfs_file = repo.get_contents(file_content.path + '.gitattributes', ref=branch_name)
                if 'filter=lfs' in lfs_file.decoded_content.decode():
                    stored_in_lfs = True
            except:
                pass
            if stored_in_lfs:
                lfs_url = f'https://api.github.com/repos/{user_name}/{repo_name}/git/blobs/{file_content.sha}'
                lfs_response = requests.get(lfs_url, headers={'Authorization': f'token {access_token}'})
                lfs_size = lfs_response.json()['size']
                size = lfs_size
            file_structure.append({"Repo Name" : repo_name,"Branch Name" : branch_name,"Directory" : directory_path,"File_Name" : file_content.name,"File_Type" : extension,"Size(Byte)" : size})
    file_structure = pd.DataFrame(file_structure, columns=["Repo Name","Branch Name","Directory", "File_Name", "File_Type", "Size(Byte)"])
    return file_structure

def list_of_github_branches(github_token, repo_owner, repo_name):
    branches = []
    g = Github(github_token)
    repo = g.get_repo(f"{repo_owner}/{repo_name}")
    for branch in repo.get_branches():
        branches.append(branch.name)
    return branches

def time_taken(start_time,today):
    end_time = time.time()
    time_taken = end_time - start_time
    today = datetime.date.today().strftime("%Y-%m-%d")
    date_df = pd.DataFrame({'Date': [today], 'Time Taken': [time_taken]})
    return date_df

branches=list_of_github_branches(github_token, repo_owner, repo_name)
with pd.ExcelWriter(f'Target_discovery_Report_{today}.xlsx',mode='w') as writer:
    get_branch_details = get_commit_info(github_token, repo_owner, repo_name)
    get_branch_details.to_excel(writer, sheet_name='Target_Branch_Info', index=False)
    for branch in branches:
        sheet_name = "Tgt_"+branch[:100]
        get_file_structure_to_excel(github_token, repo_name, branch, repo_owner).to_excel(writer, sheet_name=sheet_name, index=False)
    date_df = time_taken(start_time,today)
    date_df.to_excel(writer, sheet_name='Current Date', index=False)
