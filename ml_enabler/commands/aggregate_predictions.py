import asyncio
import click
from ml_enabler.aggregators.LookingGlassAggregator import LookingGlassAggregator

@click.command('aggregate_predictions', short_help='Aggregate predictions to lower zoom levels and add ancillary data')
@click.option('--zoom', help='Zoom level to aggregate to', type=int)
@click.option('--infile', help='Filename to read predictions JSON from', type=click.File('r'))
@click.option('--outfile', help='Filename to write results to', type=click.File('w'))
@click.option('--errfile', help='Filename to write errors to', type=click.File('w'))
@click.pass_context
def aggregate(ctx, zoom, infile, outfile, errfile):
    aggregator = LookingGlassAggregator(zoom, infile, outfile, errfile)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(aggregator.aggregate())
    print('done aggregating')
