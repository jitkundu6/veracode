import sys
import requests
from veracode_api_signing.plugin_requests import RequestsAuthPluginVeracodeHMAC
import json
import pandas as pd
import csv

api_base = "https://api.veracode.com/appsec/v2/applications/436f5986-2f37-47a3-9ebc-d9e0d2790706/summary_report"
headers = {"User-Agent": "Python HMAC Example"}


try:
    response = requests.get(api_base, auth=RequestsAuthPluginVeracodeHMAC(), headers=headers)
    r_data = dict(response.json())
    with open("summary.json", "w") as outfile:
        json.dump(r_data, outfile)  

    severity_details = json.dumps(r_data.get("severity"))
    severity = pd.read_json(severity_details)
    print(severity)

    
    header = severity_details[0].keys()
    with open("summary.csv", 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        for details in severity_details:
             writer.writerow(details.values())
    csvfile.close()

except Exception as e:
    print("ERROR: ",e)

# https://propelinc-my.sharepoint.com/:u:/p/subhajit/ETZ33BBvbqxAjBmYw8YovW8B5BW3Qu4AmaE8OsCMIySD_A?e=bgPA8Z