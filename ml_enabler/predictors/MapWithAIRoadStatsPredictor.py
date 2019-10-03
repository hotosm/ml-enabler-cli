import mercantile
import aiohttp
import asyncio
import logging
import json
from .BasePredictor import BasePredictor
from ml_enabler.utils import get_tile_quadkey, bbox_to_tiles, get_tile_center, clip_polygon
from area import area


class MapWithAIRoadStatsPredictor(BasePredictor):
    default_zoom = 16
    name = 'mapwithai_road_stats'

    async def predict(self, bbox, concurrency, outfile, errfile):
        """
        Returns MapWithAI road stats for the given bbox and tile zoom
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
        bbox_str = ','.join(map(str, bounds))
        tile_url = f'{self.tile_url}&bbox={bbox_str}'

        try:
            res = await session.get(tile_url)
            if res.status != 200:
                logging.warning(f'Unable to fetch tile {tile_url}')
                raise Exception(f'Unable to fetch tile {tile_url}')

            data = await res.json()
            return {
                'quadkey': quadkey,
                'centroid': get_tile_center(tile),
                'predictions': {
                    'ml_prediction': data['road_length_km']['total'],
                    'url': tile_url,
                }
            }
        except Exception as e:
            logging.error(str(e))
