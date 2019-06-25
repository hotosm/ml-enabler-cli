import mercantile
import aiohttp
import asyncio
import logging
import json
from .BasePredictor import BasePredictor
from ml_enabler.utils import bbox_to_polygon_wkt, get_tile_quadkey, bbox_to_tiles, get_tile_center, clip_polygon
from area import area


class BuildingPredictor(BasePredictor):
    default_zoom = 15
    name = 'building_api'

    async def predict(self, bbox, concurrency, outfile, errfile):
        """
        Returns building area for the given bbox and tile zoom
        """

        tiles = list(bbox_to_tiles(bbox, self.zoom))
        logging.info(f'Processing {len(tiles)} tiles')
        metadata = {
            'model_name': self.name,
            'version': '1.0.0',
            'bbox': bbox,
            'zoom': self.zoom
        }
        conn = aiohttp.TCPConnector(limit=concurrency)
        timeout = aiohttp.ClientTimeout(total=None, connect=None, sock_connect=None, sock_read=None)
        async with aiohttp.ClientSession(connector=conn, timeout=timeout) as session:
            futures = [self.predict_tile(session, tile) for tile in tiles]
            results = await asyncio.gather(*futures)
            data = {
                'metadata': metadata,
                'predictions': results
            }
            outfile.write(json.dumps(data, indent=2))
            outfile.close()

    async def predict_tile(self, session, tile):
        quadkey = get_tile_quadkey(tile)
        bounds = list(mercantile.bounds(tile))
        polygon_wkt = bbox_to_polygon_wkt(bounds)
        tile_url = f'{self.endpoint}?searchAreaWkt={polygon_wkt}&outputFormat=geojson'

        try:
            res = await session.get(tile_url)
            if res.status != 200:
                logging.warn(f'Unable to fetch tile {tile_url}')
                raise Exception(f'Unable to fetch tile {tile_url}')

            data = await res.json()
            # FIXME: validate data
            building_area = 0
            for feature in data['features']:
                geometry = clip_polygon(tile, feature['geometry'])
                building_area = building_area + area(geometry)

            return {
                'quadkey': quadkey,
                'centroid': get_tile_center(tile),
                'predictions': {
                    'ml_prediction': building_area,
                    'url': tile_url,
                }
            }
        except Exception as e:
            logging.error(str(e))
