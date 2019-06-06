import click
from ml_enabler.utils import bbox_to_tiles, get_building_area, get_prediction
import aiohttp
import asyncio

@click.command('fetch_predictions', short_help='Fetch model predictions for a bbox')
@click.option('--bbox', help='Bounding box to fetch predictions for, as <left>,<bottom>,<right>,<top>')
# @click.option('--tile-url', default='https://api.mapbox.com/v4/digitalglobe.2lnpeioh/{z}/{x}/{y}.jpg?access_token={token}')
@click.option('--tile-url',
              help='Tile URL to fetch tiles, eg https://api.mapbox.com/v4/mapbox.streets/{z}/{x}/{y}.jpg?access_token={token}',
              default='https://api.mapbox.com/v4/mapbox.streets/{z}/{x}/{y}.jpg?access_token={token}'
              )
@click.option('--zoom', type=int, default=8, help='Zoom level to fetch tiles at')
@click.option('--token', help='Access token for tiles URL', default=None)
@click.pass_context
def fetch(ctx, bbox, tile_url, zoom, token):
    endpoint = ctx.obj['endpoint']
    async def predict_tiles(tile_urls):
        conn = aiohttp.TCPConnector(limit=16)
        async with aiohttp.ClientSession(connector=conn) as session:
            futures = [get_prediction(session, tile_url, endpoint) for tile_url in tile_urls]
            results = await asyncio.gather(*futures)
            print('all results', results)

    def get_tile_url(tile):
        return tile_url.format(x=tile.x, y=tile.y, z=zoom, token=token)

    # print('bbox', bbox)

    tiles = list(bbox_to_tiles(bbox, zoom))
    print('no of tiles', len(tiles))
    tile_urls = list(map(get_tile_url, tiles))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(predict_tiles(tile_urls))
    print('done processing tiles')
    # asyncio.run(predict_tiles(tile_urls))

    # areas = [get_building_area(tile) for tile in tiles]
    # predictions = [get_prediction(tile_url, endpoint) for tile_url in tile_urls]





