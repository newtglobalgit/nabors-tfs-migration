import winrm
import threading
import time
import sys
import pandas as pd
import openpyxl
from credentials import cred, server, server_urls, projects

url = server.get('host')
tfs_url = server_urls.get('http_url')+'/DefaultCollection'
project_name = projects.get('project1')
username = cred.get('USER')
password = cred.get('PASSWORD')

workbook = openpyxl.Workbook()
worksheet = workbook.active
worksheet['A1'] = 'Field'
worksheet['B1'] = 'Value'

tfs_attributes = ["Branch", "Risk", "Story Points", "Stack Rank", "Resolved Reason", "Resolved By", "Resolved Date", "Finish Date", "Start Date", "Activated By", "Activated Date", "State Change Date", "Closed By", "Closed Date", "Integration Build", "Tags", "Related Link Count", "History", "Description", "Created By", "Created Date", "Work Item Type", "Assigned To", "Reason", "Changed By", "Rev", "Watermark", "Authorized Date", "State", "Title", "Authorized As", "Area ID", "ID", "Changed Date", "Revised Date", "Area Path", "Node Name", "Attached File Count", "Hyperlink Count", "Team Project", "External Link Count", "Iteration ID", "Iteration Path"]

def query_workItem(id, tfs_url):
    script2 = """$url = '%s'
    $id = '%s'
    $workItem = TFPT.EXE workitem $id /collection:$url
    | Select-String -Pattern "%s" | ConvertTo-Json
    """ % (tfs_url, id, "\n".join(f"{attr}" for attr in tfs_attributes))
    result1 = session.run_ps(script2)
    result1 = result1.std_out.decode('utf-8')
    result1 = result1.replace("\n", "").replace("<p>", "").replace("</p>", "").replace("<div>", "").replace("</div>", "").replace("<br>", "").replace("&nbsp;", "").replace("<strong>", "").replace("</strong>", "").replace("<em>", "").replace("</em>", "")
    global worksheet
    global done
    while not done:
        time.sleep(0.1)
    for row in data:
        worksheet.append(row)
    done = True

session = winrm.Session(url, auth=(username, password), transport='ntlm')
script1 = """$url = '%s'
$projectName = '%s'
$query = @"
SELECT [System.Id]
FROM WorkItems
WHERE [System.TeamProject] = '$projectName'
ORDER BY [System.Id]
"@
TFPT.EXE query /collection:$url /wiql:$query /include:data | Out-String 
""" % (tfs_url, project_name)
result = session.run_ps(script1)
result = result.std_out.decode('utf-8')
result = result.replace("\n", "").replace("<p>", "").replace("</p>", "").replace("<div>", "").replace("</div>", "").replace("<br>", "").replace("&nbsp;", "").replace("<strong>", "").replace("</strong>", "").replace("<em>", "").replace("</em>", "")
ids = result.split()
global data
data = []
threads = []
for id in ids:
    t = threading.Thread(target=query_workItem, args=(id, tfs_url))
    threads.append(t)
    t.start()
for t in threads:
    t.join()
workbook.save('work_items.xlsx')
