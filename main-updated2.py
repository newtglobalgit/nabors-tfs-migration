from asyncio.log import logger
from credentials import cred
import logging
import requests
from requests_ntlm import HttpNtlmAuth
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

username = cred.get('USER')
password = cred.get('PASSWORD')

logger.info(print("Trying to find TFS URL valid"))

TFS_URL = f"http://192.168.3.197:8080/tfs/DefaultCollection/_apis/projects?api-version=1.0"
r = requests.get(TFS_URL, verify=False)
if r.status_code == 400:
    logger.info(print("TFS domain appears to be hosted internally"))
elif r.status_code == 200:
    logger.info(print("TFS domain appears to be hosted on Azure"))

log = logging.getLogger(f"auth_tfs({username})")

headers = {"Content-Type": "text/xml"}
r = requests.get(TFS_URL, auth=HttpNtlmAuth(username, password), verify=False)
if r.status_code == 200:
    logger.info(print(f"Found credentials for User: {username}"))
else:
    logger.info(print(f"Authentication failed for User: {username} (Invalid credentials)"))
