import os
import json

from metabase.models import Metabase
from metabase.hooks import MetabaseHook

from dbt_utils import read_manifest, get_exposures, exposure_to_card

METABASE_URL = os.environ.get("METABASE_URL", "http://localhost:3000")
METABASE_API_KEY = os.environ.get(
    "METABASE_API_KEY", "mb_aCfXEEMcN2LdVzZ0d8pOz/ab2wnKFqlNqvEQf7d1vnY="
)

metabase_hook = MetabaseHook(METABASE_URL, METABASE_API_KEY)
metabase = Metabase(hook=metabase_hook)

if __name__ == "__main__":
    manifest = read_manifest(manifest_path="../target/manifest.json")

    exposures = get_exposures(manifest=manifest)

    for exposure in exposures:
        card_data = exposure_to_card(
            exposure=exposure,
            metabase=metabase,
            manifest=manifest,
        )

        print(json.dumps(card_data, indent=2))

        if not card_data:
            continue

        # metabase.hook.put("card", card_data)
        metabase.hook.post("card", card_data)
