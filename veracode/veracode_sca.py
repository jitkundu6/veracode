import sys
import requests
from veracode_api_signing.plugin_requests import RequestsAuthPluginVeracodeHMAC
import json
import pandas as pd
import csv

api_base = "https://api.veracode.com/srcclr"
# api_base = "https://api.veracode.com/appsec/v2/applications/436f5986-2f37-47a3-9ebc-d9e0d2790706/summary_report"
headers = {"User-Agent": "Python HMAC Example"}

'''
SCA API's:

workspaces
GET/v3/workspaces   #
GET/v3/workspaces/{id}
GET/v3/workspaces/{id}/issues
GET/v3/workspaces/{id}/libraries
GET/v3/workspaces/{id}/libraries/unmatched
GET/v3/workspaces/{id}/projects #
GET/v3/workspaces/{id}/projects/{projectId}
GET/v3/workspaces/{id}/projects/{projectId}/issues  #
GET/v3/workspaces/{id}/projects/{projectId}/libraries   #
GET/v3/workspaces/{id}/teams

agents
GET/v3/workspaces/{workspaceId}/agents
GET/v3/workspaces/{workspaceId}/agents/{agentId}
GET/v3/workspaces/{workspaceId}/agents/{agentId}/tokens
GET/v3/workspaces/{workspaceId}/agents/{agentId}/tokens/{tokenId}

issues
GET/v3/issues/{id}

registry
GET/v3/libraries/{id}
GET/v3/licenses/{id}
GET/v3/component-activity/{id}
GET/v3/vulnerabilities/{id}

scans
GET/v3/scans/{id}

team
GET/v3/teams
GET/v3/teams/{id}

sbom
GET/sbom/v1/targets/{targetUuid}/cyclonedx
GET/sbom/v1/targets/{targetUuid}/spdx

events
GET/v3/events
'''


try:
    response = requests.get(api_base + "/v3/workspaces", auth=RequestsAuthPluginVeracodeHMAC(), headers=headers)
    data = dict(response.json())
    data = data.get("_embedded")

    for workspace in data["workspaces"]:
        workspace.pop('_links', None)
        projects_response = requests.get(api_base + "/v3/workspaces/" + str(workspace["id"]) + "/projects", auth=RequestsAuthPluginVeracodeHMAC(), headers=headers)
        workspace["projects"] = dict(projects_response.json()).get("_embedded", dict()).get("projects")

        # issues_response = requests.get(api_base + "/v3/workspaces/" + str(workspace["id"]) + "/issues", auth=RequestsAuthPluginVeracodeHMAC(), headers=headers)
        # libraries_response = requests.get(api_base + "/v3/workspaces/" + str(workspace["id"]) + "/libraries", auth=RequestsAuthPluginVeracodeHMAC(), headers=headers)
        # teams_response = requests.get(api_base + "/v3/workspaces/" + str(workspace["id"]) + "/teams", auth=RequestsAuthPluginVeracodeHMAC(), headers=headers)
        # agents_response = requests.get(api_base + "/v3/workspaces/" + str(workspace["id"]) + "/agents", auth=RequestsAuthPluginVeracodeHMAC(), headers=headers)
        
        # workspace["issues"] = dict(issues_response.json()).get("_embedded", dict()).get("issues")
        # workspace["libraries"] = dict(libraries_response.json()).get("_embedded", dict()).get("libraries")
        # workspace["teams"] = dict(teams_response.json()).get("_embedded", dict()).get("teams")
        # workspace["agents"] = dict(agents_response.json()).get("_embedded", dict()).get("agents")

        if workspace["projects"] is None:
            continue

        for project in workspace["projects"]:  
            # GET/v3/workspaces/{id}/projects/{projectId}/issues
            issues_response = requests.get(api_base + "/v3/workspaces/" + str(workspace["id"]) + "/projects/" + str(project["id"]) + "/issues", auth=RequestsAuthPluginVeracodeHMAC(), headers=headers)
            libraries_response = requests.get(api_base + "/v3/workspaces/" + str(workspace["id"]) + "/projects/" + str(project["id"]) + "/libraries", auth=RequestsAuthPluginVeracodeHMAC(), headers=headers)
            
            project["issues"] = dict(issues_response.json()).get("_embedded", dict()).get("issues")
            project["libraries"] = dict(libraries_response.json()).get("_embedded", dict()).get("libraries")

    print(data)
    with open("sca.json", "w") as outfile:
        json.dump(data, outfile)
    
    print("SUCCESSFULLY COMPLETED.")
except Exception as e:
    print("ERROR: ",e)
