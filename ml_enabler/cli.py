import click
from ml_enabler.commands import fetch_predictions, aggregate_predictions, upload_predictions
import sys

@click.group()
# @click.option('--endpoint', default='http://localhost:8501/v1/models/looking_glass:predict')
@click.pass_context
def main_group(ctx):
    sys.stdout.write('INVOKING CLI')
    ctx.obj = {}
    # ctx.obj['endpoint'] = endpoint


main_group.add_command(fetch_predictions.fetch)
main_group.add_command(aggregate_predictions.aggregate)
main_group.add_command(upload_predictions.upload)
