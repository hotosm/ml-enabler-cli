from ml_enabler.utils import bbox_to_tiles, url_image_to_b64_string,\
                        get_raw_prediction, get_tile_center, get_tile_quadkey
from ml_enabler.utils.postproc import get_thresh_weighted_sum, get_pixel_area
from ml_enabler.exceptions import InvalidData
import aiohttp
import asyncio
import logging
import json
import numpy as np
from .BasePredictor import BasePredictor


class LookingGlassPredictor(BasePredictor):
    default_zoom = 18
    name = 'looking_glass'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.weight = self.model_opts['weight'] if 'weight' in self.model_opts else 'auto'

    async def predict(self, bbox, concurrency, outfile, errfile):
        '''
            Return predictions for given bbox
        '''
        tiles = list(bbox_to_tiles(bbox, self.zoom))
        logging.info(f'Processing {len(tiles)} tiles')
        weight = self.get_weight(bbox, self.zoom)
        conn = aiohttp.TCPConnector(limit=concurrency)
        timeout = aiohttp.ClientTimeout(total=None, connect=None, sock_connect=None, sock_read=None)
        async with aiohttp.ClientSession(connector=conn, timeout=timeout) as session:
            version = await self.get_version(session)
            metadata = {
                'model_name': self.name,
                'version': version,
                'bbox': bbox,
                'zoom': self.zoom
            }
            futures = [self.predict_tile(session, tile, weight) for tile in tiles]
            results = await asyncio.gather(*futures)
            errors = list(filter(lambda r: 'error' in r, results))
            successes = list(filter(lambda r: 'error' not in r, results))
            out_data = {
                'metadata': metadata,
                'predictions': successes
            }
            errfile.write(json.dumps(errors, indent=2))
            errfile.close()
            outfile.write(json.dumps(out_data, indent=2))
            outfile.close()

    async def predict_tile(self, session, tile, weight):
        image_url = self.tile_url.format(x=tile.x, y=tile.y, z=self.zoom, token=self.token)
        prediction_endpoint = f'{self.endpoint}models/{self.name}:predict'
        tile_centroid = get_tile_center(tile)
        quadkey = get_tile_quadkey(tile)
        try:
            payload = await self.get_payload(session, image_url)
        except Exception as e:
            logging.warning(f'Error while fetching image for quadkey {quadkey}')
            return {
                'quadkey': quadkey,
                'error': str(e),
                'error_type': 'image'
            }
        try:
            raw_prediction = await get_raw_prediction(session, prediction_endpoint, payload)
            data = self.get_data_from_prediction(raw_prediction, weight)
        except Exception as e:
            logging.warning(f'Error while fetching prediction for quadkey {quadkey}')
            return {
                'quadkey': quadkey,
                'error': str(e),
                'error_type': 'model'
            }
        # print('pred', raw_prediction)
        return {
            'quadkey': quadkey,
            'centroid': tile_centroid,
            'predictions': data
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

    async def get_version(self, session):
        version_url = f'{self.endpoint}models/{self.name}'
        res = await session.get(version_url)
        if res.status != 200:
            logging.error('Failed to fetch version information from prediction endpoint')
            raise Exception(f'Unable to fetch version information from {version_url}')
        data = await res.json()
        return data['model_version_status'][0]['version']

    def get_data_from_prediction(self, raw_prediction, weight):
        if not raw_prediction or 'predictions' not in raw_prediction:
            logging.error('Malformed data returned from prediction endpoint')
            raise InvalidData('Improper predictions format from model')
        predictions = raw_prediction['predictions']
        np_arr = np.array(predictions)
        return {
            'ml_prediction': get_thresh_weighted_sum(np_arr, weight=weight)
        }

    def get_weight(self, bbox, zoom):
        if self.weight != 'auto':
            return float(self.weight)
        else:
            latitude = float(bbox.split(',')[1])
            return get_pixel_area(latitude, zoom)
