import mercantile
from osm_task_metrics.osm import OSMData
import base64
import json
import requests
import random

def bbox_to_tiles(bbox, zoom):
    bbox_list = bbox_str_to_list(bbox)
    print('bbox_list', bbox_list)
    tiles = mercantile.tiles(*bbox_str_to_list(bbox), zooms=[zoom])
    return tiles

def bbox_str_to_list(bbox: str):
    """ Parse the bbox query param and return a list of floats """
    bboxList = bbox.split(',')
    return list(map(float, bboxList))

def get_building_area(tile):
    geojson = mercantile.feature(tile)
    return OSMData(geojson).building_area()

def tile_to_geojson(tile):
    return mercantile.feature(tile)

def get_prediction_as_float(raw_prediction):
    #FIXME: actually implement this
    return random.random()

def get_tile_quadkey(tile):
    return mercantile.quadkey(tile)

def get_tile_center(tile):
    #FIXME: actually implement this, right now returns point on a corner
    bounds = mercantile.bounds(tile)
    return [bounds.west, bounds.south]

async def get_prediction(session, tile, endpoint, zoom, token, tile_url_format):
    tile_url = tile_url_format.format(x=tile.x, y=tile.y, z=zoom, token=token)
    image_b64 = await url_image_to_b64_string(session, tile_url)
    raw_prediction = await get_raw_prediction(session, endpoint, image_b64)
    float_value = get_prediction_as_float(raw_prediction)
    tile_centroid = get_tile_center(tile)
    quadkey = get_tile_quadkey(tile)
    #print('pred', raw_prediction)
    return {
        'quadkey': quadkey,
        'center': tile_centroid,
        'data': {
            'ml_prediction': float_value,
            'osm_building_area': random.random() #FIXME
        }
    }

async def url_image_to_b64_string(session, url):
    """Convert a url to a UTF-8 coded string of base64 bytes.
    Notes
    -----
    Use this if you need to download tiles from a tile server and send them to
    a prediction server. This will convert them into a string representing
    base64 format which is more efficient than many other options.
    """
    # GET data from url
    response = await session.get(url)
    print('fetching image', url)
    if not response.status == 200:
        print('Error getting image from {}'.format(url))

    # Convert to base64 and then encode in UTF-8 for future transmission
    response_text = await response.read()
    b64 = base64.b64encode(response_text)
    b64_string = b64.decode("utf-8")
    return b64_string

async def get_raw_prediction(session, endpoint, image_b64):
    instances = [
        {
            'image_bytes': {
                'b64': image_b64
            }
        }
    ]
    payload = {'instances': instances}
    async with session.post(endpoint, json=payload) as response:
        json_response = await response.json()
        print('got prediction')
        return json_response['predictions']
