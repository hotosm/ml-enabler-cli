from ml_enabler.exceptions import InvalidModelResponse, ImageFetchError
from ml_enabler.utils.osm import OSMData
from shapely.geometry import box
import mercantile
# from osm_task_metrics.osm import OSMData
import backoff
import base64
import json
# import requests
import random

def bbox_to_tiles(bbox, zoom):
    bbox_list = bbox_str_to_list(bbox)
    tiles = mercantile.tiles(*bbox_str_to_list(bbox), zooms=[zoom])
    return tiles

def bbox_str_to_list(bbox: str):
    """ Parse the bbox query param and return a list of floats """
    bboxList = bbox.split(',')
    return list(map(float, bboxList))

async def get_building_area(session, tile):
    geojson = mercantile.feature(tile)
    return await OSMData(geojson).building_area(session)

def tile_to_geojson(tile):
    return mercantile.feature(tile)

def get_tile_quadkey(tile):
    return mercantile.quadkey(tile)

def get_tile_center(tile):
    bbox = mercantile.bounds(tile)
    return f'SRID=4326;{box(bbox[0], bbox[1], bbox[2], bbox[3]).centroid.wkt}'

@backoff.on_exception(backoff.expo, ImageFetchError, max_tries=3)
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
        raise ImageFetchError()

    # Convert to base64 and then encode in UTF-8 for future transmission
    response_text = await response.read()
    b64 = base64.b64encode(response_text)
    b64_string = b64.decode("utf-8")
    return b64_string

@backoff.on_exception(backoff.expo, InvalidModelResponse, max_tries=5)
async def get_raw_prediction(session, endpoint, payload):
    async with session.post(endpoint, json=payload) as response:
        if response.status != 200:
            raise InvalidModelResponse(response.status)
        json_response = await response.json()
        return json_response

def bbox_to_polygon_wkt(bbox: list):
    """ Get a polygon from the bbox """

    return box(bbox[0], bbox[1], bbox[2], bbox[3]).wkt