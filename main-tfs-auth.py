import logging
import requests
from requests_ntlm import HttpNtlmAuth
from requests.exceptions import ConnectionError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

username = 'jayakarthi'
password = 'orkut2009@'
TfsServer = '192.168.3.197'
NameOfCollection = 'DefaultCollection'
NameOfProject = 'DPROG'
tfsApi = 'http://192.168.3.197:8080/tfs/DefaultCollection/_apis/projects?api-version=2.0'
#          http://192.168.3.197:8080/tfs/DefaultCollection/_apis/projects?api-version=2.0

def auth(self, username, password):
    log = logging.getLogger(f"auth_owa({username})")

    headers = {"Content-Type": "text/xml"}
    session = requests.Session()
    session.auth = HttpNtlmAuth('username','password')
    r = session.get('http://192.168.3.197:8080/tfs')

    if r.status_code == 200:
        log.info(print(f"Found credentials: {username}:{password}"))
        self.valid_accounts.add(f'{username}:{password}')
    else:
        log.info(print(f"Authentication failed: {username}:{password} (Invalid credentials)")) 

""" tfsResponse = requests.get(tfsApi,auth=HttpNtlmAuth(username,password),verify=False)
if(tfsResponse.ok):
    tfsResponse = tfsResponse.json()
    print(tfsResponse)
else:
    tfsResponse.raise_for_status() """