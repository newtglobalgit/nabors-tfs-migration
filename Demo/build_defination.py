# import requests
# import json

# # Define the URL of the build definition in your TFS instance
# build_definition_url = 'http://192.168.3.197:8080/tfs/DefaultCollection/CatCore/_apis/build/definitions/3?api-version=5.1'

# # Define the GitHub repository and branch where you want to create the new workflow file
# github_repository = 'https://github.com/UjjAwal021/CatCore.git'
# github_branch = 'cleanup'

# # Get the build definition from your TFS instance
# response = requests.get(build_definition_url, auth=('ujjawal', 'Trade@1234'))

# if response.status_code != 200:
#     print(f"Failed to get the build definition: {response.text}")
#     exit()

# build_definition = response.json()

# # Create the GitHub Actions workflow file
# workflow = {
#     'name': 'Build and Test',
#     'on': 'push',
#     'jobs': {
#         'build': {
#             'runs-on': 'ubuntu-latest',
#             'steps': [
#                 {'name': 'Checkout code', 'uses': 'actions/checkout@v2'},
#             ]
#         }
#     }
# }

# # Add steps to the GitHub Actions workflow file for each step in the build definition
# for phase in build_definition['phases']:
#     for step in phase['steps']:
#         if step['task']['definitionType'] == 'task':
#             task_name = step['task']['friendlyName']
#             task_version = step['task']['version']['major']
#             task_id = step['task']['id']
#             task_inputs = step['inputs']
#             step_name = f'{task_name} (v{task_version})'

#             # Map TFS tasks to GitHub Actions steps
#             if task_id == '71a9a2d3-a98a-4caa-96ab-affca411ecda':  # Visual Studio Build task
#                 workflow['jobs']['build']['steps'].append({
#                     'name': step_name,
#                     'run': f'msbuild {task_inputs["solution"]} /p:Configuration={task_inputs["configuration"]} /p:Platform={task_inputs["platform"]}'
#                 })
#             elif task_id == 'd781d02f-eb43-4aea-b6fb-aa7cab8de099':  # Visual Studio Test task
#                 workflow['jobs']['build']['steps'].append({
#                     'name': step_name,
#                     'run': f'vstest {task_inputs["testAssembly"]} /Platform:{task_inputs["platform"]} /Framework:{task_inputs["testFramework"]}'
#                 })
#             # Add more TFS tasks to GitHub Actions steps mapping as needed

# # Convert the workflow dictionary to YAML format and write it to a file
# workflow_yaml = json.dumps(workflow, indent=2).replace('\'', '').replace('"', '').replace('\n', '\n  ')
# with open('.github/workflows/build.yml', 'w') as f:
#     f.write(f'on:\n  {workflow["on"]}\njobs:\n  {json.dumps(workflow["jobs"], indent=2)}\n')



# Import TFS libraries
from Microsoft.TeamFoundation.Client import TfsTeamProjectCollection
from Microsoft.TeamFoundation.Build.Client import BuildServer

# Replace these variables with your own values
tfsUrl = "http://tfs2013:8080/tfs/DefaultCollection"
teamProjectName = "MyTeamProject"
buildDefinitionName = "MyBuildDefinition"

# Connect to TFS
tfsCollection = TfsTeamProjectCollection(tfsUrl)
tfsCollection.EnsureAuthenticated()

# Get the build server
buildServer = BuildServer(tfsCollection)

# Get the team project
teamProject = buildServer.GetTeamProject(teamProjectName)

# Get the build definition
buildDefinition = teamProject.QueryBuildDefinitions(buildDefinitionName)

if buildDefinition:
    print("Build definition found:")
    print(buildDefinition[0].Name)
else:
    print("Build definition not found.")
