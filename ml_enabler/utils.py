import mercantile
from osm_task_metrics.osm import OSMData
import requests
import base64
import json

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

def get_prediction(tile_url, endpoint):
    image_b64 = url_image_to_b64_string(tile_url)
    raw_prediction = get_raw_prediction(endpoint, image_b64)
    print('predicted', tile_url)
    #print('pred', raw_prediction)
    return raw_prediction

def url_image_to_b64_string(url):
    """Convert a url to a UTF-8 coded string of base64 bytes.
    Notes
    -----
    Use this if you need to download tiles from a tile server and send them to
    a prediction server. This will convert them into a string representing
    base64 format which is more efficient than many other options.
    """
    # GET data from url
    response = requests.get(url)
    if not response.ok:
        print('Error getting image from {}'.format(url))

    # Convert to base64 and then encode in UTF-8 for future transmission
    b64 = base64.b64encode(response.content)
    b64_string = b64.decode("utf-8")
    return b64_string

def get_raw_prediction(endpoint, image_b64):
    instances = [
        {
            'image_bytes': {
                'b64': image_b64
            }
        }
    ]
    payload = json.dumps({'instances': instances})
    response = requests.post(endpoint, data=payload)
    return json.loads(response.content)['predictions']