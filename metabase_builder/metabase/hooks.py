from email.policy import default
import os
import json
import requests
from typing import List, Dict, Any


from metabase.models import Database, Table, Field, Card

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

    def get_databases(self) -> Dict[int, Database]:
        '''Lists databases in Metabase.'''
        databases = [Database(**database) for database in self.get(endpoint='database')['data']]
        databases = {database.id: database for database in databases}
        return databases

    def get_tables(self) -> Dict[int, Table]:
        '''Lists tables in Metabase.'''
        tables = [
            table for table in self.get(endpoint='table')
        ]
        tables = [Table(**table) for table in tables]
        tables = {table.id: table for table in tables}
        return tables

    def get_database_fields(self, database_id) -> Dict[int, Field]:
        fields = [Field(**field) for field in self.get(endpoint=f'database/{database_id}/fields')]
        fields = {field.id: field for field in fields}
        return fields

    def get_cards(self) -> Dict[int, Card]:
        '''Lists cards (questions) in Metabase.'''
        cards = self.get(endpoint='card')

        # TODO: How to deal with it?
        for card in cards:
            if 'last-edit-info' in card:
                card.pop('last-edit-info')

        # TODO: Can be question, model or metric
        cards = [
            Card(**card) for card in cards
            if card['type'] == 'question'
        ]
        cards = {card.id: card for card in cards}
        return cards

    def get_card(self, card_id):
        return self.get(endpoint=f'card/{card_id}')
