import os
import requests
from dotenv import load_dotenv
import sys
from datetime import datetime

load_dotenv()

access_pat = os.getenv('PAT')
gitlab_url = os.getenv('GITLAB_URL')
project_id = os.getenv('PROJ_ID')

days_expire_max = int(sys.argv[1])

req_header = {'PRIVATE-TOKEN' : access_pat}
req_url = gitlab_url + '/api/v4/projects/' + project_id + '/access_tokens/'
try:
    pat_raw = requests.get(req_url, headers=req_header).json()
    for token in pat_raw:
        if token['active'] == True and token['revoked'] == False:
            date_diff=(datetime.strptime(token['expires_at'], "%Y-%m-%d") - datetime.today()).days
            if date_diff < days_expire_max:
                print(f"Token {token['name']} id {token['id']} expires at {token['expires_at']} in {date_diff} days, less than {days_expire_max} days. ")
                sys.exit(1)
    print(f"Seems all active tokens for this project are fine now.")
except Exception as e:
    print(e)
    sys.exit(1)
