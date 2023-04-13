import os, time ,dateutil
import pandas as pd
from tfs import TFSAPI
from requests_ntlm import HttpNtlmAuth
from datetime import datetime
import datetime, get_list_of_branch
from credentials import cred, path, server_urls

tfs_url = server_urls.get('http_url')
username = cred.get('USER')
password = cred.get('PASSWORD')
source_dir_path = path.get('source_dir')

start_time = time.time()
def get_folder_info(root_folder_path):
    global tfs_url
    root_folder_path = os.path.abspath(os.path.join(root_folder_path, os.pardir))
    folder_info_list = []
    root_folder_name = os.path.basename(root_folder_path)
    branches = get_list_of_branch.get_list_of_branches_path(tfs_url) 
    branches = [b.replace('/', '\\') for b in branches] 
    for root, dirs, files in os.walk(root_folder_path):
        if any("$tf" in d for d in root.split(os.sep)):
            continue
        subfolder_depth = len(os.path.relpath(root, root_folder_path).split(os.sep))
        if subfolder_depth > 15:
            continue 
        for dir in dirs:
            if "$tf" in dir:
                continue
            subfolder_path = os.path.join(root, dir)
            subfolder_name = os.path.basename(subfolder_path)
            parent_folder_path = os.path.relpath(os.path.abspath(os.path.join(subfolder_path, os.pardir)), root_folder_path)
            parent_folder_path = parent_folder_path.replace('/', '\\') 
            if parent_folder_path in branches:
                subfolder_type = "Branch"
            else:
                subfolder_type = "Folder"
            folder_info_list.append([parent_folder_path, subfolder_name, "", subfolder_type, ""])
        for file in files:
            file_path = os.path.join(root, file)
            file_name = os.path.basename(file_path)
            file_extension = os.path.splitext(file_name)[1]
            file_size = os.path.getsize(file_path)  
            parent_folder_path = os.path.relpath(os.path.abspath(os.path.join(file_path, os.pardir)), root_folder_path)
            parent_folder_path = parent_folder_path.replace('/', '\\') 
            subfolder_name = os.path.basename(root)
            folder_info_list.append([parent_folder_path, subfolder_name, file_name, file_extension, file_size])
    df = pd.DataFrame(folder_info_list, columns=['ParentFolder', 'SubFolder', 'FileName', 'Type', 'FileSize(Byte)'])
    return df

tfs = TFSAPI(tfs_url, user=username, password=password, auth_type=HttpNtlmAuth)

commit_info_list = []

branches = get_list_of_branch.get_list_of_branches(tfs_url)
branch_count = 0
for branch in branches:
    branch_count += 1
    print(branch)
changesets = tfs.get_changesets(item_path=branch)
last_commit_date = None
total_commit_count = 0
last_author_name = None

branches = get_list_of_branch.get_list_of_branches(tfs_url)
for branch in branches:
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
    
    # Calculate BranchStatus based on last commit date and commit count
    branch_status = 'inactive'
    # da = (datetime.datetime.utcnow() - dateutil.parser.parse(last_commit_date)).days
    # if total_commit_count >= 10 and da <= 365:
    if (datetime.datetime.utcnow() - dateutil.parser.parse(last_commit_date)).days<=365:
        branch_status = 'active'
    
    branch_name = branch.split('/')[-1]

    commit_info_list.append({'Branch Name': branch_name, 'Branch path': branch, 'Total commit count': total_commit_count, 'Last Commit Date': last_commit_date, 'Last Cimmit By': last_author_name, 'BranchStatus': branch_status})


commit_df = pd.DataFrame(commit_info_list, columns=['Branch Name', 'Branch path', 'Total commit count', 'Last Commit Date', 'Last Cimmit By', 'BranchStatus'])


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
        commit_messages_branch.append({'Branch': branch, 'Commit ID': changeset_id, 'Commit Date & Time': date, 'Commit Message': comment, 'Author': author_name})
    commit_messages_df_branch = pd.DataFrame(commit_messages_branch, columns=['Branch', 'Commit ID', 'Commit Date & Time', 'Commit Message', 'Author'])
    commit_messages.append((branch, commit_messages_df_branch))


end_time = time.time()
time_taken = end_time - start_time
today = datetime.date.today().strftime("%Y-%m-%d")
date_df = pd.DataFrame({'Date': [today], 'Time Taken': [time_taken]})

with pd.ExcelWriter(f'Discovery_Report_{today}.xlsx', mode='w') as writer:
    
    commit_df.to_excel(writer, sheet_name='Branch Info', index=False)
    for branch in branches:
        commit_messages_df_branch = [x[1] for x in commit_messages if x[0] == branch][0]
        commit_messages_df_branch = pd.DataFrame(commit_messages_df_branch, columns=['Branch', 'Commit Date & Time', 'Commit Message', 'Author'])
        branch_name = branch.split('/')[-1]
        sheet_name = f'{branch_name}_Commits'
        commit_messages_df_branch.to_excel(writer, sheet_name=sheet_name, index=False)
    date_df.to_excel(writer, sheet_name='Current Date', index=False)
    get_folder_info(source_dir_path).to_excel(writer, sheet_name='Folder Info', index=False)