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
