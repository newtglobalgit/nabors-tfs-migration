# import os
# import shutil

# project_dir = "C:\TFS\Practice\DPROG"

# # A list of file extensions to include
# extensions = ['.txt', '.csv', '.bin', '.dat', '.exe']

# # Initialize an empty list to store file paths
# file_paths = []

# # Traverse the directory and search for files with the specified extensions
# for root, dirs, files in os.walk(project_dir):
#     for filename in files:
#         if any(filename.endswith(ext) for ext in extensions):
#             file_paths.append(os.path.join(root, filename))

# # Print the list of file paths
# # print(file_paths)




# new_dir = "C:/TFS/tfs-migration12"

# # Iterate over the list of file paths and copy each file to the new directory
# for path in file_paths:
#     # Get the filename from the path
#     filename = os.path.basename(path)
#     # Copy the file to the new directory
#     shutil.copy(path, os.path.join(new_dir, filename))


import shutil
import os

# Define source and destination folders
source_folder = "C:\TFS\Practice\DPROG"
destination_folder = "C:\TFS\\tfs-migration12"

# Get a list of files in the source folder
files = os.listdir(source_folder)

# Loop through the files and copy them to the destination folder
for file_name in files:
    # Create the full file paths
    source_file_path = os.path.join(source_folder, file_name)
    destination_file_path = os.path.join(destination_folder, file_name)
    
    print(source_file_path)
    print(destination_file_path)
    # Copy the file to the destination folder
    shutil.copytree(source_folder, destination_folder)
