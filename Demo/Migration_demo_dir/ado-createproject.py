from azure.devops.connection import Connection
from azure.devops.v6_0.core.models import TeamProject
from msrest.authentication import BasicAuthentication
from credentials import ado, projects

organization = ado.get('org1')
project = projects.get('project5')
token = ado.get('token')

credentials = BasicAuthentication('', token)
connection = Connection(base_url=f"https://dev.azure.com/{organization}", creds=credentials)

core_client = connection.clients.get_core_client()

project_name = "catcore-demo"
project_description = "This is a new project created with Python"
project_capabilities = {
    "versioncontrol": {
        "sourceControlType": "Tfvc"
    },
    "processTemplate": {
        "templateTypeId": "49b62771-11cf-4507-9101-1bd680434da7"
    }
    }

new_project = TeamProject(name=project_name, description=project_description, capabilities=project_capabilities, visibility='private')

created_project = core_client.queue_create_project(new_project)

print("New project created with ID:", created_project.id)
