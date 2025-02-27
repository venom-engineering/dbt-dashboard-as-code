import os
import json

from metabase.models import Metabase
from metabase.hooks import MetabaseHook

from dbt_utils import read_manifest, get_exposures, exposure_to_card

METABASE_URL = os.environ.get('METABASE_URL', 'http://localhost:3000')
METABASE_API_KEY = os.environ.get('METABASE_API_KEY', 'mb_eB0jYj/56l6HGbMWZ6ICfkytAKRnQFjBRRyBh9hsB2k=')
MANIFEST_PATH = '../../target/manifest.json'

metabase_hook = MetabaseHook(METABASE_URL, METABASE_API_KEY)
metabase = Metabase(hook=metabase_hook)

if __name__ == '__main__':
    manifest = read_manifest(manifest_path=MANIFEST_PATH)

    exposures = get_exposures(manifest=manifest)

    for exposure in exposures:
        card_data = exposure_to_card(
            exposure=exposure,
            metabase=metabase,
            manifest=manifest,
        )

        if not card_data:
            continue

        card = [
            card for card_id, card in metabase.cards.items()
            if card.exposure_unique_id == exposure.unique_id
        ]

        if card:
            card = card[0]
            metabase.hook.put(f'card/{card.id}', card_data)
        else:
            metabase.hook.post('card/', card_data)
