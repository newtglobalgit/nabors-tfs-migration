from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
import os

path = 'C:\TFS\Practice\DPROG' 

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