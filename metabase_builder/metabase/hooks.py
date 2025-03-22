from email.policy import default
import os
import json
import requests
from typing import List, Dict, Any


class MetabaseHook:

    def __init__(
                self,metabase_url: str,
                metabase_api_key: str,
        ) -> None:
        self.metabase_url = metabase_url
        self.metabase_api_key = metabase_api_key

    def get(self, endpoint: str) -> Any:
        '''Retrieves objects from a Metabase API endpoint.'''
        url = f'{self.metabase_url}/api/{endpoint}'
        headers = {
            'x-api-key': self.metabase_api_key,
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f'Error retrieving objects from {endpoint}: {e}')
            return {}

    def put(self, endpoint: str, data: Dict) -> Any:
        '''Put objects from a Metabase API endpoint.'''
        url = f'{self.metabase_url}/api/{endpoint}'
        headers = {
            'x-api-key': self.metabase_api_key,
            'Content-Type': 'application/json',
        }
        data_string = json.dumps(data, default=str)

        try:
            response = requests.put(url, headers=headers, data=data_string)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f'Error retrieving objects from {endpoint}: {e}')
        return {}

    def post(self, endpoint: str, data: Dict) -> Any:
        '''Post objects from a Metabase API endpoint.'''
        url = f'{self.metabase_url}/api/{endpoint}'
        headers = {
            'x-api-key': self.metabase_api_key,
            'Content-Type': 'application/json',
        }
        data_string = json.dumps(data, default=str)

        try:
            response = requests.post(url, headers=headers, data=data_string)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f'Error retrieving objects from {endpoint}: {e}')
        return {}
