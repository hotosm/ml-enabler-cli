import asyncio
import click
from ml_enabler.aggregators import aggregators
import logging
# from ml_enabler.aggregators.LookingGlassAggregator import LookingGlassAggregator
import sys


@click.command('aggregate_predictions', short_help='Aggregate predictions to lower zoom levels and add ancillary data')
@click.option('--name', help='Name of the aggregator', type=str)
@click.option('--zoom', help='Zoom level to aggregate to', type=int)
@click.option('--overpass-url',
              help='URL for Overpass server - eg. https://lz4.overpass-api.de/api/interpreter',
              default='https://lz4.overpass-api.de/api/interpreter'
              )
@click.option('--infile', help='Filename to read predictions JSON from', type=click.File('r'))
@click.option('--outfile', help='Filename to write results to', type=click.File('w'))
@click.pass_context
def aggregate(ctx, name, zoom, overpass_url, infile, outfile):
    if not outfile:
        logging.error('You must provide an outfile to write results to')
        sys.exit(1)
    if not name:
        logging.error('You must provide the name of the aggregator to use')
        sys.exit(1)
    aggregator_class = aggregators[name]
    try:
        aggregator = aggregator_class(zoom, overpass_url, infile, outfile)
    except ValueError as e:
        logging.error(str(e))
        sys.exit(1)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(aggregator.aggregate())
    logging.info('Done aggregating')
