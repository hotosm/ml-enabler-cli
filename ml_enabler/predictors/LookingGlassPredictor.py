from ml_enabler.utils import bbox_to_tiles, url_image_to_b64_string,\
                        get_raw_prediction, get_tile_center, get_tile_quadkey
from ml_enabler.utils.postproc import get_thresh_weighted_sum
from ml_enabler.exceptions import InvalidData
import aiohttp
import asyncio
import json
import numpy as np
from .BasePredictor import BasePredictor

class LookingGlassPredictor(BasePredictor):
    default_zoom = 18

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.weight = self.model_opts['weight'] if 'weight' in self.model_opts else 'auto'

    async def predict(self, bbox, concurrency, outfile, errfile):
        '''
            Return predictions for given bbox
        '''
        tiles = list(bbox_to_tiles(bbox, self.zoom))
        print(f'Processing {len(tiles)} tiles')
        weight = self.get_weight(bbox)
        conn = aiohttp.TCPConnector(limit=concurrency)
        timeout = aiohttp.ClientTimeout(total=None, connect=None, sock_connect=None, sock_read=None)
        async with aiohttp.ClientSession(connector=conn, timeout=timeout) as session:
            futures = [self.predict_tile(session, tile, weight) for tile in tiles]
            results = await asyncio.gather(*futures)
            errors = list(filter(lambda r: 'error' in r, results))
            successes = list(filter(lambda r: 'error' not in r, results))
            errfile.write(json.dumps(errors, indent=2))
            errfile.close()
            outfile.write(json.dumps(successes, indent=2))
            outfile.close()
        
    async def predict_tile(self, session, tile, weight):
        image_url = self.tile_url.format(x=tile.x, y=tile.y, z=self.zoom, token=self.token)
        tile_centroid = get_tile_center(tile)
        quadkey = get_tile_quadkey(tile)
        try:
            payload = await self.get_payload(session, image_url)
        except Exception as e:
            return {
                'quadkey': quadkey,
                'error': str(e),
                'error_type': 'image'
            }
        try:    
            raw_prediction = await get_raw_prediction(session, self.endpoint, payload)
            data = self.get_data_from_prediction(raw_prediction, weight)
        except Exception as e:
            return {
                'quadkey': quadkey,
                'error': str(e),
                'error_type': 'model'
            }
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

    def get_data_from_prediction(self, raw_prediction, weight):
        if not raw_prediction or 'predictions' not in raw_prediction:
            raise InvalidData('Improper predictions format from model')        
        predictions = raw_prediction['predictions']
        np_arr = np.array(predictions)
        return {
            'ml_prediction': get_thresh_weighted_sum(np_arr, weight=weight)
        }

    def get_weight(self, bbox):
        #FIXME: if auto, calculate weight based on latitude
        if self.weight != 'auto':
            return float(self.weight)
        else: #FIXME: calculate 'auto'
            return 0.76

