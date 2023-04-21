# secrets / sensitive data store

cred = {
    'USER': "", ## TFS windows User credentials
    'PASSWORD': "", ## TFS windows User credentials
    'token': "", ## GITHUB Organization user token
    'api_base_url': "https://api.github.com",
    'owner': "" ## GITHUB Organization user
}

data = {
    "name": "catcore",
    "description": "migration repository",
    "private": False,
    "directory_path": 'ascii'
}

urls = {
    'http_url': "http://192.168.3.197:8080/tfs/DefaultCollection/{projects}/_apis/_versionControl",
    'https_url': "https://192.168.3.197/tfs/DefaultCollection/_apis/tfvc/repositories"
}

server_urls = {
    'http_url': "http://192.168.3.197:8080/tfs",
    'https_url': "https://192.168.3.197/tfs"
}

ado = {
    'org1': "NewtADTF",
    'token': "" ## ADO organization token

}

path = {
    'repos': "C:/Users/Administrator/Source/Repos/",
    'loc_repo': "C:/TFS/tfs-migration12",
    'source_dir': "C:\Discovery"
}

server = {
    'host': "http://192.168.3.197",
    'https_url': "https://192.168.3.197",
    'windows_user': "" ## Windows local user
}

projects = {
    'project1': "DPROG",
    'project2': "Demo",
    'project3': "tfs-test",
    'project4': "Sample_Practice_Project",
    'project5': "CatCore",
    'project6': "tfs-ado"
}