import requests
from credentials import cred, data

personal_access_token = cred.get('token')
api_base_url = cred.get('api_base_url')
owner = cred.get('owner')
repo = data.get('name')

response = requests.post(f"{api_base_url}/user/repos", json=data, headers={
    "Authorization": f"Bearer {personal_access_token}"
})

if response.status_code == 201:
    print("Successfully created repository")
else:
    print("Failed to create repository")

file_path = "dummy.txt"
file_content = "This is the content of the file"

response = requests.put(f"{api_base_url}/repos/{owner}/{repo}/contents/{file_path}")