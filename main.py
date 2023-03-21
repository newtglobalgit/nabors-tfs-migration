import requests
from tfs import TFSAPI
from requests_ntlm import HttpNtlmAuth
from credentials import cred, server, path,projects

# Specify the URL of the TFS server and the project collection
tfs_url = 'http://192.168.3.197:8080/tfs'
project_collection = 'DefaultCollection'
# tfs_url = server.get('host')
username = cred.get('USER')
password = cred.get('PASSWORD')

# Specify the project you want to analyze
project_name = 'DPROG'

# Create an instance of the TFSAPI class to connect to the TFS server
tfs = TFSAPI(tfs_url, user=username, password=password, auth_type=HttpNtlmAuth)


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


folder_path = "$/dprog/infinity.net"
count_files(folder_path)

# import tfs

# # Connect to the TFS collection and get a reference to the folder
# tfs = tfs.connect('http://192.168.3.197:8080/tfs')
# folder_path = '$/dprog/infinity.net'
# folder_item = tfs.get_item(folder_path)

# # Initialize counters for ASCII and binary files
# ascii_count = 0
# binary_count = 0

# # Iterate over each item in the folder and count the number of ASCII and binary files
# for item in folder_item.items():
#     # Determine whether the item is a file
#     if item.is_file:
#         # Determine whether the file is ASCII or binary
#         if item.extension in ('.txt', '.csv', '.log'):
#             ascii_count += 1
#         else:
#             # Read the contents of the file and check for non-ASCII characters
#             with item.download_file() as f:
#                 is_binary = any(ord(c) > 127 for c in f.read(1024))
#                 if is_binary:
#                     binary_count += 1

# # Print the counts
# print(f'ASCII files: {ascii_count}')
# print(f'Binary files: {binary_count}')
