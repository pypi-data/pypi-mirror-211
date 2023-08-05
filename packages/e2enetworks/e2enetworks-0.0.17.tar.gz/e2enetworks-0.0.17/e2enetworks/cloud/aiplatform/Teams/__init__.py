import json

import requests

from e2enetworks.cloud.aiplatform import config
from e2enetworks.constants import BASE_GPU_URL, INDENTATION


class Teams:
    def create(self, team_name):
        payload = json.dumps({
            "team_name": team_name,
        })
        url = f"{BASE_GPU_URL}teams/?apikey={config.apikey}"

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {config.auth_token}'
        }
        response = requests.request("POST", url, headers=headers, data=payload)

        print(json.dumps(response.json(), indent=INDENTATION))
        #return response.json()

    def get(self, team_id):
        url = f"{BASE_GPU_URL}teams/{team_id}/?apikey={config.apikey}"
        payload = ""
        headers = {
            'Authorization': f'Bearer {config.auth_token}'
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        print(json.dumps(response.json(), indent=INDENTATION))
        #return response.json()

    def list(self):
        url = f"{BASE_GPU_URL}teams/?apikey={config.apikey}"
        payload = ""
        headers = {
            'Authorization': f'Bearer {config.auth_token}'
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        print(json.dumps(response.json(), indent=INDENTATION))
        #return response.json()

    def delete(self, team_id):
        url = f"{BASE_GPU_URL}teams/{team_id}/?apikey={config.apikey}"
        payload = ""
        headers = {
            'Authorization': f'Bearer {config.auth_token}'
        }
        response = requests.request("DELETE", url, headers=headers, data=payload)
        print(json.dumps(response.json(), indent=INDENTATION))
        #return response.json()
