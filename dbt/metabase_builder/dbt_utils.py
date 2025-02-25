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

    for node_id in exposure.depends_on['nodes']:

        node = manifest['nodes'][node_id]

        metabase_table_id = [
            table_id for table_id, table in metabase.tables.items()
            if (
                metabase.databases[table.db_id].name == node['database']
                and table.schema == node['schema']
                and table.name == node['alias']
            )
        ]
        break

    if metabase_table_id:
        metabase_table_id = metabase_table_id[0]
    else:
        return None

    card = meta.get('metabase')
    if not card:
        return None

    metadata_description = {'exposure_id': exposure.unique_id}
    description = card.get('description', '')
    if description:
        description += '\n\n'

    card['description'] = f'{description}{metadata_description}'


    dataset_query = {
        'database': metabase.tables[metabase_table_id].db_id,
        'type': 'query',
        'query': {
            'source-table': metabase_table_id,
            'aggregation': [],
            'breakout': [],
            'order-by': [],
        },
    }
    query = card.pop('_query')

    # Get only fields from dependencies
    filtered_fields = {
        field.name: field
        for _, field in metabase.fields.items()
        if field.table_id == 11
    }

    for aggregation in query['aggregation']:
        field = filtered_fields[aggregation['field']]
        dataset_query['query']['aggregation'].append([
            aggregation['type'], ['field', field.id, {'base-type': field.base_type}],
        ])

    for breakout in query['breakout']:
        field = filtered_fields[breakout['field']]
        dataset_query['query']['breakout'].append([
            'field', field.id, {'base-type': field.base_type},
        ])

    for order_by in query['order_by']:
        field = filtered_fields[breakout['field']]
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
