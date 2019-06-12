import asyncio
import click
from ml_enabler.predictors.LookingGlassPredictor import LookingGlassPredictor

@click.command('fetch_predictions', short_help='Fetch model predictions for a bbox')
@click.option('--bbox', help='Bounding box to fetch predictions for, as <left>,<bottom>,<right>,<top>')
# @click.option('--tile-url', default='https://api.mapbox.com/v4/digitalglobe.2lnpeioh/{z}/{x}/{y}.jpg?access_token={token}')
@click.option('--tile-url',
              help='Tile URL to fetch tiles, eg https://api.mapbox.com/v4/mapbox.streets/{z}/{x}/{y}.jpg?access_token={token}',
              default='https://api.mapbox.com/v4/mapbox.streets/{z}/{x}/{y}.jpg?access_token={token}'
              )
@click.option('--zoom', type=int, default=8, help='Zoom level to fetch tiles at')
@click.option('--token', help='Access token for tiles URL', default=None)
@click.option('--concurrency', help='Number of simultaneous requests to make to prediction image', type=int, default=16)
@click.option('--outfile', help='Filename to write results to', type=click.File('w'))
@click.option('--errfile', help='Filename to write errors to', type=click.File('w'))
@click.pass_context
def fetch(ctx, bbox, tile_url, zoom, token, concurrency, outfile, errfile):
    endpoint = ctx.obj['endpoint']
    predictor = LookingGlassPredictor(endpoint, tile_url, token)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(predictor.predict(bbox, concurrency, outfile, errfile))
    print('done processing tiles')





