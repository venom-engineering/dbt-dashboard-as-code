import functools

import click

from cli import params
# TODO: move somewhere else
from metabase_builder.dbt_utils import (exposure_to_card, get_exposures,
                                        read_manifest)
from metabase_builder.metabase.hooks import MetabaseHook
from metabase_builder.metabase.metabase import Metabase


# approach from https://github.com/pallets/click/issues/108#issuecomment-280489786
def global_flags(func):
    @params.url
    @params.api_key
    @params.manifest_path
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


@click.group(
    context_settings={"help_option_names": ["-h", "--help"]},
    invoke_without_command=True,
    no_args_is_help=True,
    epilog="Specify one of these sub-commands and you can find more help from there.",
)
@click.pass_context
@global_flags
def cli(ctx, **kwargs):
    # TODO: add help description
    """
    CLI for generating dashboard.
    """


@cli.command("run")
@click.pass_context
@global_flags
def run(ctx, **kwargs):
    """
    Generate dashboard.
    """
    metabase = Metabase(hook=MetabaseHook(kwargs['url'], kwargs['api_key']))
    manifest = read_manifest(manifest_path=kwargs['manifest_path'])

    exposures = get_exposures(manifest=manifest)

    for exposure in exposures:
        card_data = exposure_to_card(
            exposure=exposure,
            metabase=metabase,
            manifest=manifest,
        )

        if not card_data:
            continue

        card = metabase.get_card_by_exposure_id(exposure.unique_id)

        if card:
            metabase.hook.put(f'card/{card.id}', card_data)
        else:
            metabase.hook.post('card/', card_data)

    print("Runned")

@cli.command("info")
@click.pass_context
@global_flags
def info(ctx, **kwargs):
    """
    Get card info
    """
    import pprint
    metabase = Metabase(hook=MetabaseHook(kwargs['url'], kwargs['api_key']))

    pprint.pprint(metabase.hook.get(endpoint='card',))


if __name__ == "__main__":
    cli()
