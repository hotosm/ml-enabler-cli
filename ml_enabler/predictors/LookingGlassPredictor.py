from ml_enabler.utils import bbox_to_tiles, get_building_area, url_image_to_b64_string,\
                        get_raw_prediction, get_tile_center, get_tile_quadkey
from ml_enabler.utils_postproc import get_thresh_weighted_sum
import aiohttp
import asyncio
import json
import numpy as np
from .BasePredictor import BasePredictor

class LookingGlassPredictor(BasePredictor):
    zoom = 18

    async def predict(self, bbox, concurrency, outfile):
        '''
            Return predictions for given bbox
        '''
        tiles = list(bbox_to_tiles(bbox, self.zoom))
        print(f'Processing {len(tiles)} tiles')
        conn = aiohttp.TCPConnector(limit=concurrency)
        timeout = aiohttp.ClientTimeout(total=None, connect=None, sock_connect=None, sock_read=None)
        async with aiohttp.ClientSession(connector=conn, timeout=timeout) as session:
            futures = [self.predict_tile(session, tile) for tile in tiles]
            results = await asyncio.gather(*futures)
            outfile.write(json.dumps(results, indent=2))
            outfile.close()
        
    async def predict_tile(self, session, tile):
        image_url = self.tile_url.format(x=tile.x, y=tile.y, z=self.zoom, token=self.token)
        payload = await self.get_payload(session, image_url)
        raw_prediction = await get_raw_prediction(session, self.endpoint, payload)
        data = self.get_data_from_prediction(raw_prediction)
        tile_centroid = get_tile_center(tile)
        quadkey = get_tile_quadkey(tile)
        #print('pred', raw_prediction)
        return {
            'quadkey': quadkey,
            'center': tile_centroid,
            'data': data
        }
    
    async def get_payload(self, session, image_url):
        image_base64 = await url_image_to_b64_string(session, image_url)
        instances = [
            {
                'image_bytes': {
                    'b64': image_base64
                }
            }
        ]
        return {
            'instances': instances
        }

    def get_data_from_prediction(self, raw_prediction):
        if raw_prediction and 'predictions' in raw_prediction:
            predictions = raw_prediction['predictions']
            np_arr = np.array(predictions)
            return {
                'ml_prediction': get_thresh_weighted_sum(np_arr)
            }
        else:
            return {
                'error': 'Error fetching prediction'
            }


