from ml_enabler.aggregators.BaseAggregator import BaseAggregator
from ml_enabler.utils import get_building_area
import mercantile
import aiohttp
import asyncio
import json
import logging


class BuildingAggregator(BaseAggregator):

    async def aggregate(self):
        conn = aiohttp.TCPConnector(limit=3)
        timeout = aiohttp.ClientTimeout(total=None, connect=None, sock_connect=None, sock_read=None)
        async with aiohttp.ClientSession(connector=conn, timeout=timeout) as session:
            futures = [self.get_values_for_quadkey(session, prediction) for prediction in self.source_data]
            results = await asyncio.gather(*futures)
            data = {
                'metadata': self.source_metadata,
                'predictions': results
            }
            self.outfile.write(json.dumps(data, indent=2))
            self.outfile.close()

    async def get_values_for_quadkey(self, session, prediction):

        quadkey = prediction['quadkey']
        tile = mercantile.quadkey_to_tile(prediction['quadkey'])
        osm_building_area = await get_building_area(session, tile, self.overpass_url)
        return {
            'quadkey': quadkey,
            'centroid': prediction['centroid'],
            'predictions': {
                **prediction['predictions'],
                **{'osm_building_area': osm_building_area}
            }
        }
