import click
from ml_enabler.commands import fetch_predictions, aggregate_predictions, upload_predictions
from ml_enabler import __version__


@click.group()
@click.version_option(version=__version__, message='%(version)s')
@click.pass_context
def main_group(ctx):
    ctx.obj = {}
    # ctx.obj['endpoint'] = endpoint


main_group.add_command(fetch_predictions.fetch)
main_group.add_command(aggregate_predictions.aggregate)
main_group.add_command(upload_predictions.upload)
