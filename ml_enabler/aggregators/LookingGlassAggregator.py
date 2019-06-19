from ml_enabler.aggregators.BaseAggregator import BaseAggregator
from ml_enabler.utils import get_building_area, get_tile_center
import functools
import mercantile
import aiohttp
import asyncio
import json


class LookingGlassAggregator(BaseAggregator):
    async def aggregate(self):
        agg_quadkeys = self.get_agg_quadkeys()
        conn = aiohttp.TCPConnector(limit=3)  # FIXME: make concurrency a param
        timeout = aiohttp.ClientTimeout(total=None, connect=None, sock_connect=None, sock_read=None)
        async with aiohttp.ClientSession(connector=conn, timeout=timeout) as session:
            futures = [self.get_values_for_quadkey(session, quadkey) for quadkey in agg_quadkeys]
            results = await asyncio.gather(*futures)
            self.source_metadata['zoom'] = self.zoom
            out_data = {
                'metadata': self.source_metadata,
                'predictions': results
            }
            self.outfile.write(json.dumps(out_data, indent=2))
            self.outfile.close()

    def get_agg_quadkeys(self):
        '''
            Returns the list of unique quadkeys in the dataset at the destination zoom level
        '''
        all_quadkeys = [d['quadkey'] for d in self.source_data]
        return list(set([q[0:self.zoom] for q in all_quadkeys]))

    async def get_values_for_quadkey(self, session, quadkey):
        '''
            Returns consolidated data values for a quadkey
        '''
        filtered_quadkeys = list(
            filter(lambda d: d['quadkey'].startswith(quadkey), self.source_data))
        total_ml_building_area = functools.reduce(
            lambda a, b: int(a + b['predictions']['ml_prediction']),
            filtered_quadkeys,
            0)
        tile = mercantile.quadkey_to_tile(quadkey)
        osm_building_area = await get_building_area(session, tile, self.overpass_url)
        return {
            'quadkey': quadkey,
            'centroid': get_tile_center(tile),
            'predictions': {
                'ml_prediction': total_ml_building_area,
                'osm_building_area': osm_building_area
            }
        }
