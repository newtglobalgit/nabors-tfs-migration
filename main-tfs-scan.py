from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
import os
# from credentials import cred, server_urls, projects

# # Fill in your TFS organization URL and personal access token
# # (you can generate a PAT from your TFS account settings)
# tfs_url = server_urls.get('http_url')


# user = cred.get('USER')
# password = cred.get('PASSWORD')

# # Create a connection to TFS using basic authentication
# credentials = BasicAuthentication(user,password)
# connection = Connection(base_url=tfs_url, creds=credentials)

# # Fill in the project name and the path to the folder containing the files
# project_name = projects.get('project1')
# folder_path = "$/DPROG"

# # Get the version control client
# # vc_client = connection.clients.get_client()

# vc_client = connection.clients.get_client()

# # Get the items in the folder (recursively)
# items = vc_client.get_items(path=folder_path, recursion_level='Full')

# # Loop through the items and download any files
# for item in items:
#     if item.is_file:
#         # Construct the local path for the file
#         local_path = os.path.join("local", "path", item.server_item.replace(folder_path, ""))
        
#         # Download the file content
#         with open(local_path, "wb") as f:
#             stream = vc_client.get_file_content(item.server_item)
#             f.write(stream.readall())

path = 'C:\TFS\Practice\DPROG'  # file path
 
# # using basename function from os
# # module to print file name
# file_name = os.path.basename(file_path)
 
# print(file_name)


# files = os.listdir(path)

# for file in files:
#     print(file)

def list_files(path):
    file_list = []
    for root, directories, files in os.walk(path):
        for filename in files:
            file_path = os.path.join(root, filename)
            file_list.append(file_path)
    return file_list

path = 'C:\TFS\Practice\DPROG'
files = list_files(path)

for file in files:
    print(file)
