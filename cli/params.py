import os

import click

url = click.option(
    "--url",
    envvar="METABASE_URL",
    help="Url of Metabase instance. Use this flag or set 'METABASE_URL' env var",
)

api_key = click.option(
    "--api-key",
    envvar="METABASE_API_KEY",
    help="API Key of Metabase instance. Use this flag or set 'METABASE_API_KEY' env var",
)

manifest_path = click.option(
    "--manifest-path",
    default="./target/manifest.json",
    help="Path to dbt's manifest.json file",
)

