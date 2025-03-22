from typing import Any, Dict, List, Optional

from .definitions import Card, Database, Field, Table


class Metabase:

    def __init__(self, hook):
        self.hook = hook

        self.refresh_state()

    def refresh_state(self):
        # Get all Metabase objects
        self._databases = self.get_databases()
        self._tables = self.get_tables()
        self._fields = self.get_databases_fields()

        self._cards = self.get_cards()

        self._dashboards = ...
        self._users = ...  # ?
        self._tiles = ...  # ?
        self._datasets = ...  # ?

    @property
    def databases(self):
        return self._databases

    def get_database_by_id(self, id):
        return self._databases[id]

    @property
    def tables(self):
        return self._tables

    def get_table_by_id(self, id):
        return self._tables[id]

    def get_table_by_node(self, node):
        matched_tables = [
            table for _, table in self.tables.items()
            if (
                table.db.name == node['database']
                and table.schema == node['schema']
                and table.name == node['alias']
            )
        ]
        if not matched_tables:
            print(f'No table match for node: {node["unique_id"]}')
            return None
        elif len(matched_tables) > 1:
            raise Exception(f'Multiple tables match for node: {node["unique_id"]}')
        else:
            return matched_tables[0]

    @property
    def fields(self):
        return self._fields

    @property
    def cards(self):
        return self._cards

    def get_card_by_exposure_id(self, exposure_unique_id):
        matched_cards = [
            card for _, card in self.cards.items()
            if card.exposure_unique_id == exposure_unique_id
        ]
        if not matched_cards:
            ...  # print(f'No card match for exposure: {exposure_unique_id}')
            return None
        elif len(matched_cards) > 1:
            raise Exception(f'Multiple cards match for exposure: {exposure_unique_id}')
        else:
            return matched_cards[0]

    def get_databases(self) -> Dict[int, Database]:
        '''Lists databases in Metabase.'''
        databases = [Database(metabase=self, **database) for database in self.hook.get(endpoint='database').get('data', [])]
        databases = {database.id: database for database in databases}
        return databases

    def get_tables(self) -> Dict[int, Table]:
        '''Lists tables in Metabase.'''
        tables = [
            table for table in self.hook.get(endpoint='table')
        ]
        tables = [Table(metabase=self, **table) for table in tables]
        tables = {table.id: table for table in tables}
        return tables

    def get_cards(self) -> Dict[int, Card]:
        '''Lists cards (questions) in Metabase.'''
        cards = self.hook.get(endpoint='card')

        # TODO: How to deal with it?
        for card in cards:
            if 'last-edit-info' in card:
                card.pop('last-edit-info')

        # TODO: Can be question, model or metric
        cards = [
            Card(metabase=self, **card) for card in cards
            if card['type'] == 'question'
        ]
        cards = {card.id: card for card in cards}
        return cards

    def get_databases_fields(self):
        fields = {}
        for database_id, _ in self._databases.items():
            database_fields = [Field(metabase=self, **field) for field in self.hook.get(endpoint=f'database/{database_id}/fields')]
            database_fields = {field.id: field for field in database_fields}
            fields.update(database_fields)
        return fields
