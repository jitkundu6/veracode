import sys
import requests
from veracode_api_signing.plugin_requests import RequestsAuthPluginVeracodeHMAC
import pandas as pd
import json

api_base = "https://api.veracode.com/appsec/v2/applications/436f5986-2f37-47a3-9ebc-d9e0d2790706/summary_report"
headers = {"User-Agent": "Python HMAC Example"}


try:
    response = requests.get(api_base, auth=RequestsAuthPluginVeracodeHMAC(), headers=headers)
    print(dict(response.json()))
    jobj = json.dumps(response.json())
    # data = pd.read_json(jobj)
except Exception as e:
    print("ERROR: ",e)