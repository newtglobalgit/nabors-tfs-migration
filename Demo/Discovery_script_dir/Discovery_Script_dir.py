'''
Discovery script
'''
import os
import time
import dateutil
import pandas as pd
import datetime, get_list_of_branch
from tfs import TFSAPI
from requests_ntlm import HttpNtlmAuth
from credentials import cred, path, server_urls, projects

tfs_url = server_urls.get('http_url')
username = cred.get('USER')
password = cred.get('PASSWORD')
source_dir_path = path.get('source_dir')
project = projects.get('project5')
source_dir_path = os.path.join(source_dir_path, project)
github_token = cred.get('token')
repo_owner = cred.get('owner')
files_list = []

start_time = time.time()
today = datetime.date.today().strftime("%Y-%m-%d")



def get_folder_info(path,project,branch):
    global files_list
    rows = []
    root_path = os.path.join(path.split(project)[0], project)
    for root, dirs, files in os.walk(path):

        level = root.replace(path, '').count(os.sep)
        dir_path = root.replace(root_path, "").lstrip('\\')
        if ".git" in dirs:
            dirs.remove(".git")  
        if ".github" in dirs:
            dirs.remove(".github")
        for file in files:
            if file == ".gitattributes":
                continue  
            filename = os.path.join(root, file)
            files_list.append(filename)
            size = os.path.getsize(filename)
            file_type = os.path.splitext(filename)[1]
            Repo_Name = project
            Branch = branch
            rows.append([Repo_Name,Branch,dir_path, file, file_type, size])
    return pd.DataFrame(rows, columns=["Repo Name","Branch Name","Directory", "File_Name", "File_Type", "Size(Byte)"])



get_list_of_branch.migration(project, source_dir_path)
tfs = TFSAPI(tfs_url, user=username, password=password, auth_type=HttpNtlmAuth)

commit_info_list = []

branches_with_folder = get_list_of_branch.get_branches_and_folders()
branches = get_list_of_branch.get_list_of_branches(tfs_url)
temp = get_list_of_branch.get_list_of_branches(tfs_url)

branch_count = 0
for branch in branches:
    branch_count += 1
    print(branch)
changesets = tfs.get_changesets(item_path=branch)
last_commit_date = None
total_commit_count = 0
last_author_name = None

for branch_idx, branch in enumerate(branches):
    changesets = tfs.get_changesets(item_path=branch)
    last_commit_date = None
    total_commit_count = 0
    last_author_name = None

    for changeset in changesets:
        try:
            changeset_id = changeset['changesetId']
            author_name = changeset['author']['displayName']
            comment = changeset['comment']
        except KeyError:
            comment = '<no comment>'
        date = changeset['createdDate']
        total_commit_count += 1
        if last_commit_date is None or date > last_commit_date:
            last_commit_date = date
            last_author_name = author_name

        if last_commit_date is not None:
            try:
                last_commit_date = last_commit_date.replace('T', ' ').replace('Z', '')[:19]
            except AttributeError:
                print(f"Warning: Invalid date format: {last_commit_date}")
        else:
            last_commit_date = '<no date>'
    
    branch_status = 'inactive'
    if (datetime.datetime.utcnow() - dateutil.parser.parse(last_commit_date)).days<=180:
        branch_status = 'active'
    
    branch_name = branch.split('/')[-1]
    if branch in temp: 
        branch_id = f"Branch{branch_idx+1}"
    else:
        branch_id = f"Folder"
    
    missing_branches = set(branches_with_folder) - set(branch.split('/')[-1] for branch in branches)
    for missing_branch in missing_branches:
        branches.append(f'$/{project}/{missing_branch}')
    
    Repo_Name = project
        
    commit_info_list.append({'Repo Name' : Repo_Name, 'Branch Name': branch_name,'Branch ID': branch_id, 'Branch path': branch, 'Total commit count': total_commit_count, 'Last Commit Date': last_commit_date, 'Last Commit By': last_author_name, 'BranchStatus': branch_status})


commit_df = pd.DataFrame(commit_info_list, columns=['Repo Name','Branch Name','Branch ID', 'Branch path', 'Total commit count', 'Last Commit Date', 'Last Commit By', 'BranchStatus'])

commit_messages = []
for branch in branches:
    changesets = tfs.get_changesets(item_path=branch)
    commit_messages_branch = []
    for changeset in changesets:
        changeset_id = changeset['changesetId']
        author_name = changeset['author']['displayName']
        comment = changeset['comment']
        date = changeset['createdDate']
        if date is not None:
            try:
                date = date.replace('T', ' ').replace('Z', '')[:19]
            except AttributeError:
                print(f"Warning: Invalid date format: {date}")
        else:
            date = '<no date>'
        Repo_Name = project
        commit_messages_branch.append({'Repo Name': project,'Branch': branch, 'Commit ID': changeset_id, 'Commit Date & Time': date, 'Commit Message': comment, 'Author': author_name})
    commit_messages_df_branch = pd.DataFrame(commit_messages_branch, columns=['Branch', 'Commit ID', 'Commit Date & Time', 'Commit Message', 'Author'])
    commit_messages.append((branch, commit_messages_df_branch))


def time_taken(start_time,today):
    end_time = time.time()
    time_taken = end_time - start_time
    date_df = pd.DataFrame({'Date': [today], 'Time Taken': [time_taken]})
    return date_df

with pd.ExcelWriter(f'Source_discovery_Report_{today}.xlsx', mode='w') as writer:
    
    commit_df.to_excel(writer, sheet_name='Source_Branch_Info', index=False)

    # get_branch_details = Github_discovery_script.get_commit_info(github_token, repo_owner, project)
    # get_branch_details.to_excel(writer, sheet_name='Target_Branch_Info', index=False)

    for branch in branches_with_folder:
        branch_path = os.path.join(source_dir_path, branch)
        get_folder_info(branch_path,project,branch).to_excel(writer, sheet_name="src_"+branch, index=False)

    # git_branches = Github_discovery_script.list_of_github_branches(github_token, repo_owner, project)
    # for branch in git_branches:
    #     sheet_name = "tgt_"+branch[:100]
    #     Github_discovery_script.get_file_structure_to_excel(github_token, project, branch, repo_owner).to_excel(writer, sheet_name=sheet_name, index=False)

    for branch in branches:
        commit_messages_df_branch = [x[1] for x in commit_messages if x[0] == branch][0]
        commit_messages_df_branch = pd.DataFrame(commit_messages_df_branch, columns=['Branch', 'Commit Date & Time', 'Commit Message', 'Author'])
        branch_name = branch.split('/')[-1]
        sheet_name = f'src_{branch_name}_Cmt'
        commit_messages_df_branch.to_excel(writer, sheet_name=sheet_name, index=False)
        
    date_df = time_taken(start_time,today)
    date_df.to_excel(writer, sheet_name='Current Date', index=False)
