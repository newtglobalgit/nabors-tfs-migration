# secrets / sensitive data store

cred = {
    'USER': "", ## Windows server credentials
    'PASSWORD': "", ## Windows server credentials
    'token': "", ## GITHUB personal access token
    'api_base_url': "https://api.github.com",
    'owner': "", ## GITHUB Organization User ID
    'org': "" ## GITHUB Organization name
}

server = {
    'host': "http://192.168.3.197",
    'https_url': "https://192.168.3.197"
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
    'csv_file' : "C://demo-tfs//Demo//extension.csv",
    'git_repo' : "https://github.com/{owner}/CatCore.git",
    'git_repo_path' : "C://Demo//usr//CatCore",
    'script_path': "C://development//demo//"
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

ado = {
    'org1': "",
    'token': ""
}