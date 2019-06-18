import asyncio
import click
from ml_enabler.aggregators import aggregators
# from ml_enabler.aggregators.LookingGlassAggregator import LookingGlassAggregator


@click.command('aggregate_predictions', short_help='Aggregate predictions to lower zoom levels and add ancillary data')
@click.option('--name', help='Name of the aggregator', type=str)
@click.option('--zoom', help='Zoom level to aggregate to', type=int)
@click.option('--infile', help='Filename to read predictions JSON from', type=click.File('r'))
@click.option('--outfile', help='Filename to write results to', type=click.File('w'))
@click.option('--errfile', help='Filename to write errors to', type=click.File('w'))
@click.pass_context
def aggregate(ctx, name, zoom, infile, outfile, errfile):
    aggregatorClass = aggregators[name]
    aggregator = aggregatorClass(zoom, infile, outfile, errfile)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(aggregator.aggregate())
    print('done aggregating')
