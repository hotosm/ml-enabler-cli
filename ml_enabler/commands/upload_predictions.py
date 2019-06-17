import click
import json

@click.command('aggregate_predictions', short_help='Aggregate predictions to lower zoom levels and add ancillary data')
@click.option('--infile', help='Filename to read predictions JSON from', type=click.File('r'))
@click.option('--api-url', help='ML Enabler API URL', default='http://localhost:8000/')
@click.pass_context
def upload(ctx, infile, api_url):

    
