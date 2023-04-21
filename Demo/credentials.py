"""
  Secrets / Sensitive data store
"""

cred = {
    'USER': "",
    'PASSWORD': "",
    'token': "",
    'api_base_url': "https://api.github.com",
    'owner': ""
}

data = {
    "name": "CatCore",
    "description": "migration repository",
    "private": False,
    "directory_path": 'ascii'
}

urls = {
    'http_url': "http://192.168.3.197:8080/tfs/DefaultCollection/{projects}/_apis/_versionControl",
    'https_url': "https://192.168.3.197/tfs/DefaultCollection/_apis/tfvc/repositories"
}

server_urls = {
    'http_url': "http://192.168.3.197:8080/tfs/",
    'https_url': "https://192.168.3.197/tfs/"
}

path = {
    'repos': "C:/Users/Administrator/Source/Repos/",
    'loc_repo': "C:/TFS/tfs-migration12",
    'csv_file' : r"C:\Final_Script\extension.csv",
    'git_repo' : "https://github.com/{owner}/CatCore.git",
    'git_repo_path' : "C://usr//CatCore"
}

commit = {
    'message': "dummy folder creation"
}

server = {
    'host': "http://192.168.3.197",
    'https_url': "https://192.168.3.197"
}

projects = {
    'project1': "dprog",
    'project2': "Demo",
    'project3': "tfs-test",
    'project4': "Sample_Practice_Project",
    'project5': "CatCore"
}
