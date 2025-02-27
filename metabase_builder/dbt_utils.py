import json
from dataclasses import dataclass
from typing import List, Dict, Literal, Any

@dataclass
class DbtExposure:
    name: str
    resource_type: str
    package_name: str
    path: str
    original_file_path: str
    unique_id: str
    fqn: List[str]

    type: Literal['dashboard', 'notebook', 'analysis', 'ml', 'application']
    maturity: Literal['low', 'medium', 'high']
    owner: Dict[str, str]
    description: str
    url: str
    label: Dict[str, str]
    tags: List[str]

    meta: Dict

    config: Dict
    unrendered_config: Any

    depends_on: Dict
    refs: List
    sources: List
    metrics: List
    created_at: float


def exposure_to_card(exposure, metabase, manifest):

    meta = exposure.meta

    card = meta.get('metabase')

    if not card:
        return None

    # Get Metabase source table assuming only one table source.
    # TODO: joins are not supported yet.
    node_id = exposure.depends_on['nodes'][0]
    node = manifest['nodes'][node_id]
    table = metabase.get_table_by_node(node)

    if not table:
        print(f'Need to create Metabase table for node: {node_id}')
        return None

    reformat_card(exposure, card, table)

    return card


def reformat_card(exposure, card, table):
    # Override description to set the exposure unique ID.
    # This is the only way we found to match states between runs.
    meta_description = f'\n\nexposure_unique_id: {exposure.unique_id}'
    card['description'] = card.get('description', '') + meta_description

    # Format dataset query.
    dataset_query = {
        'database': table.db_id,
        'type': 'query',
        'query': {
            'source-table': table.id,
            'aggregation': [],
            'breakout': [],
            'order-by': [],
        },
    }

    # Get only fields from dependencies
    fields_dict = {
        field.name: field for field in table.fields
    }

    _query = card.pop('_query')

    for aggregation in _query['aggregation']:
        field = fields_dict[aggregation['field']]
        dataset_query['query']['aggregation'].append([
            aggregation['type'], ['field', field.id, {'base-type': field.base_type}],
        ])

    for breakout in _query['breakout']:
        field = fields_dict[breakout['field']]
        dataset_query['query']['breakout'].append([
            'field', field.id, {'base-type': field.base_type},
        ])

    for order_by in _query['order_by']:
        field = fields_dict[breakout['field']]
        dataset_query['query']['order-by'].append([
            order_by['mode'], [order_by['from'], order_by['index']],
        ])

    card['dataset_query'] = dataset_query

    return card


def read_manifest(manifest_path):
    with open(manifest_path, 'r') as f:
        manifest = json.load(f)
    return manifest


def get_exposures(manifest):

    exposures_data = manifest.get('exposures', {})
    exposures = [
        DbtExposure(**exposure) for exposure in exposures_data.values()
    ]
    return exposures
