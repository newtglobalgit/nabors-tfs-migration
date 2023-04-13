import os
import subprocess
import pandas as pd

def get_folder_info(root_folder_path):
    global tfs_url
    root_folder_path = os.path.abspath(os.path.join(root_folder_path, os.pardir))
    folder_info_list = []
    root_folder_name = os.path.basename(root_folder_path)

    # Get list of workspaces on TFS server
    cmd = f"tf workspaces /collection:{tfs_url}"
    result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    workspaces = result.stdout.strip().split('\n')[1:]

    # Get list of mappings in each workspace
    for workspace in workspaces:
        owner, computer, comment = workspace.split()
        cmd = f"tf workspaces /owner:{owner} /computer:{computer} /collection:{tfs_url} /format:detailed"
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        mappings = result.stdout.strip().split('\n\n')[1:]

        # Extract folder paths from mappings
        for mapping in mappings:
            path = mapping.split('\n')[0].split(': ')[1]
            path = path.replace('$', root_folder_name, 1)  # Replace $ with root folder name
            path = os.path.normpath(path)  # Normalize path
            if not os.path.isdir(path):
                continue
            subfolder_type = "Branch" if path != root_folder_path else "Folder"

            # Add folder info to list
            subfolder_name = os.path.basename(path)
            parent_folder_path = os.path.relpath(os.path.abspath(os.path.join(path, os.pardir)), root_folder_path)
            parent_folder_path = parent_folder_path.replace('/', '\\')
            folder_info_list.append([parent_folder_path, subfolder_name, "", subfolder_type, ""])

    # Traverse file system and add file/folder info to list
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
            if not os.path.isdir(subfolder_path):
                continue
            subfolder_name = os.path.basename(subfolder_path)
            parent_folder_path = os.path.relpath(os.path.abspath(os.path.join(subfolder_path, os.pardir)), root_folder_path)
            parent_folder_path = parent_folder_path.replace('/', '\\')
            subfolder_type = "Branch" if parent_folder_path in branches else "Folder"
            folder_info_list.append([parent_folder_path, subfolder_name, "", subfolder_type, ""])
        for file in files:
            file_path = os.path.join(root, file)
            file_name = os.path.basename(file_path)
            file_extension = os.path.splitext(file_name)[1]
            file_size = os.path.getsize(file_path)
            parent_folder_path = os.path.relpath(os.path.abspath(os.path.join(file_path, os.pardir)), root_folder_path)
            parent_folder_path = parent_folder_path.replace('/', '\\')
            subfolder_name = os.path.basename(root)
            folder_info_list.append([parent_folder_path])