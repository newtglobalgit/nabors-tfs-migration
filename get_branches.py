import requests
from credentials import cred, server, path, projects

username = cred.get('USER')
password = cred.get('PASSWORD')
tfs_url = server.get('host')
defpath = path.get('repos')
path = defpath.strip()
project_name = projects.get('project1')


# api_url = f"{tfs_url}/{project_name}/_apis/git/repositories/{repository_id}/refs?api-version=6.0"
# response = requests.get(api_url, auth=(username, password))


# if response.status_code == 200:
#     branches = []
#     response_json = response.json()
#     for item in response_json["value"]:
#         if item["name"].startswith("refs/heads/"):
#             branches.append(item["name"][11:])
#     print(branches)
# else:
#     print("An error occurred:")
#     print(response.content.decode())


repository_name = "MyRepository"

# Define the API URL to get the repository ID
api_url = f"{tfs_url}:8080/tfs/DefaultCollection/{project_name}/_versionControl#path=%24%2Fdprog%2Finfinity.net&_a=contents"

# Make an HTTP GET request to the API
response = requests.get(api_url, auth=(username, password))
# http://servername:8080/tfs/DefaultCollection/projectname/_apis/git/repositories?api-version=6.0

# Parse the JSON response and find the repository ID
if response.status_code == 200:
    response_json = response.json()
    for item in response_json["value"]:
        if item["name"] == repository_name:
            repository_id = item["id"]
            break
    print(f"The repository ID for {repository_name} is {repository_id}.")
else:
    print("An error occurred:")
    print(response.content.decode())
