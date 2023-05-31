import sys
import requests
from veracode_api_signing.plugin_requests import RequestsAuthPluginVeracodeHMAC
import pandas as pd
import json

api_base = "https://api.veracode.com/appsec/v2/applications/436f5986-2f37-47a3-9ebc-d9e0d2790706/summary_report"
headers = {"User-Agent": "Python HMAC Example"}


# if __name__ == "__main__":
try:
    response = requests.get(api_base, auth=RequestsAuthPluginVeracodeHMAC(), headers=headers)
except requests.RequestException as e:
    print("Whoops!")
    print(e)
    sys.exit(1)

if response.ok:
    data = dict(response.json())
    datas = dict()
    # print(data)
    for key in data.keys():
        d = data.get(key)
        datas[key] = pd.DataFrame(d)
    
    print(datas)

    # data = pd.read_json(json_object)
    # for app in data["_embedded"]["applications"]:
    #     print(app["profile"]["name"])
else:
    print(response.status_code)
