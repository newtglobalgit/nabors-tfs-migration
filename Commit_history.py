from tfs import TFSAPI
from credentials import cred, server, path,projects
from requests_ntlm import HttpNtlmAuth
import pprint

tfs_url = "http://192.168.3.197:8080/tfs"
username = cred.get('USER')
password = cred.get('PASSWORD')

headers = {
    'Content-Type': 'application/json',
}

tfs = TFSAPI(tfs_url, user=username, password=password, auth_type=HttpNtlmAuth)
print(tfs)

changesets = tfs.get_changesets()

branch_name = tfs.tfvc.get_branch()[0]['name']
print(branch_name)


for changeset in changesets:
    pprint.pprint(changeset)
    try:
        changeset_id = changeset['changesetId']
        uniqueName = changeset['author']['uniqueName']
        comment = changeset['comment']
        date = changeset['createdDate']
    except KeyError:
        comment = '<no comment>'
    print(f'Changeset ID: {changeset_id}')
    print(f'uniqueName: {uniqueName}')
    print(f'Comment: {comment}')
    print(f'Date: {date}')




