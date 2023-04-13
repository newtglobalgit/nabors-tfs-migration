import winrm
from credentials import cred, server, server_urls


url = server.get('host')
tfs_url = server_urls.get('http_url')+'DefaultCollection'
project_name = 'tfs-ado'
username = cred.get('USER')
password = cred.get('PASSWORD')

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
TFPT.EXE query /collection:$url /wiql:$query /include:data
""" % (tfs_url, project_name)

output = session.run_ps(script1)
work_item_id = []

work_item_id = utf_decode(output)

work_items = []
for item in work_item_id:

    work_item = {
        'id': item,
        # 'title': fields[1],
        # 'state': fields[2]
    }
    work_items.append(work_item)


def query_workItem(id, tfs_url):
    script2 = """$url = '%s'
    $id = '%s'
    TFPT.EXE workitem $id /collection:$url
    """ % (tfs_url, id)

    result = session.run_ps(script2)
    return result.std_out.decode('utf-8')
    # print(result.std_out.decode('utf-8'))
    # print("query executed")

# Open a file for writing
with open('output.txt', 'w') as f:
    for work_item in work_items:
        result = query_workItem(work_item['id'], tfs_url)

        print(work_item['id'])
        print(result)

        # Write the work_item['id'] and result to the file
        f.write(f"{work_item['id']}: {result}\n")
