import pytfsclient
from tfs import TFSAPI

tfs_url = 'http://192.168.3.197:8080/tfs'
project_collection = 'DefaultCollection'

# Specify the project you want to analyze
project_name = 'DPROG'

# Create an instance of the TFSAPI class to connect to the TFS server
tfs = TFSAPI(tfs_url, project_collection)

# Define a recursive function to count the number of ASCII and binary files in a folder
def count_files(folder_path):
    ascii_count = 0
    binary_count = 0

    # Get the folder item from TFS
    folder_item = tfs.get_item(folder_path)

    # Loop through each item in the folder and count the number of ASCII and binary files
    for item in folder_item['children']:
        # If the item is a file, determine if it's ASCII or binary
        if item['is_file']:
            if item['content_type'] == 'text/plain':
                ascii_count += 1
            else:
                binary_count += 1
        # If the item is a folder, recursively count the files in that folder
        else:
            subfolder_path = item['path']
            subfolder_ascii_count, subfolder_binary_count = count_files(subfolder_path)
            ascii_count += subfolder_ascii_count
            binary_count += subfolder_binary_count

    return ascii_count, binary_count
