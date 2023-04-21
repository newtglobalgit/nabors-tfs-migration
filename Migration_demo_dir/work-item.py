import winrm, threading, time, sys
import pandas as pd
import openpyxl
from credentials import cred, server, server_urls, projects

url = server.get('host')
tfs_url = server_urls.get('http_url')+'DefaultCollection'
project_name = projects.get('project5')
username = cred.get('USER')
password = cred.get('PASSWORD')
workbook = openpyxl.Workbook()
worksheet = workbook.active

worksheet['A1'] = 'Field'
worksheet['B1'] = 'Value'

def utf_decode(output):
    if output.status_code == 0:
        regular_string = output.std_out.decode('utf-8')
        trimmed_string = regular_string.strip()
        work_item_ids = trimmed_string.split('\n')
        for id in work_item_ids:
            work_item_id.append(id.strip())
        return work_item_id
    else:
        print('Error running PowerShell script: %s' % output.std_err.decode('utf-8'))

session = winrm.Session(url, auth=(username, password), transport='ntlm')
script1 = """$url = '%s'
$projectName = '%s'
$query = @"
SELECT [System.Id] 
FROM WorkItems 
WHERE [System.TeamProject] = '$projectName'
ORDER BY [System.Id]
"@
TFPT.EXE query /collection:$url /wiql:$query /include:data | Out-String -stream
""" % (tfs_url, project_name)

output = session.run_ps(script1)
work_item_id = []
work_item_id = utf_decode(output)
work_items = []
for item in work_item_id:
    work_item = {
        'id': item,
    }
    work_items.append(work_item)

tfs_attributes = ["Branch", "Risk", "Story Points", "Stack Rank", "Resolved Reason", "Resolved By", "Resolved Date", "Finish Date", "Start Date", "Activated By", "Activated Date", "State Change Date", "Closed By", "Closed Date", "Integration Build", "Tags", "Related Link Count", "History", "Description", "Created By", "Created Date", "Work Item Type", "Assigned To", "Reason", "Changed By", "Rev", "Watermark", "Authorized Date", "State", "Title", "Authorized As", "Area ID", "ID", "Changed Date", "Revised Date", "Area Path", "Node Name", "Attached File Count", "Hyperlink Count", "Team Project", "External Link Count", "Iteration ID", "Iteration Path"]

def query_workItem(id, tfs_url, attr):
    script2 = f"TFPT.EXE workitem '{id}' /collection:'{tfs_url}' | Select-String -Pattern '{attr} =' -Context 0, 0"
    result = session.run_ps(script2)
    result = result.std_out.decode('iso-8859-1')
    # result = result.std_out.decode('utf-8')
    result = result.replace("\n", "")
    result = result.replace("\r", "")

    if len(result) > 0:
        lines = result.split("\n")
        value = None
        for line in lines:
            if line.strip().startswith(f"{attr} ="):
                try:
                    value = line.strip().split(" = ")[1]
                except IndexError:
                    value = None
                break
        return value
    else:
        return ""


data = []

for work_item in work_items:
    # row = {'ID': work_item['id']}
    row = {}
    for attr in tfs_attributes:
        value = query_workItem(work_item['id'], tfs_url, attr)
        row[attr] = value
    data.append(row)

df = pd.DataFrame(data)

with pd.ExcelWriter(f'Work_items_{project_name}.xlsx') as writer:
    df.to_excel(writer, index=False)