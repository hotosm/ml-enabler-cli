from ml_enabler.utils import bbox_str_to_list, get_tile_center, bbox_to_polygon_wkt, clip_polygon
import mercantile
import json


def test_bbox_str_to_list():
    bbox_str = '12.45,75.23,11.67,76.89'
    assert(bbox_str_to_list(bbox_str)) == [12.45, 75.23, 11.67, 76.89]


def test_get_tile_center():
    tile = mercantile.Tile(39, 72, 7)
    assert(get_tile_center(tile)) == 'SRID=4326;POINT (-68.90625 -23.23509017801799)'


def test_bbox_to_polygon_wkt():
    tile = mercantile.Tile(39, 72, 7)
    bounds = mercantile.bounds(tile)
    assert bbox_to_polygon_wkt(list(bounds)) == 'POLYGON ((-67.5 -24.5271348225978, -67.5 -21.94304553343818, -70.3125 -21.94304553343818, -70.3125 -24.5271348225978, -67.5 -24.5271348225978))'  # noqa


def test_clip_polygon():
    tile = mercantile.Tile(39, 72, 7)
    polygon = {
        "type": "Polygon",
        "coordinates": [
          [
            [
              -68.5711669921875,
              -23.79539759797873
            ],
            [
              -66.7254638671875,
              -23.79539759797873
            ],
            [
              -66.7254638671875,
              -22.61908160971607
            ],
            [
              -68.5711669921875,
              -22.61908160971607
            ],
            [
              -68.5711669921875,
              -23.79539759797873
            ]
          ]
        ]
      }

    polygon_outside = {
        "type": "Polygon",
        "coordinates": [
          [
            [
              -69.927978515625,
              -20.76638681251519
            ],
            [
              -69.400634765625,
              -20.76638681251519
            ],
            [
              -69.400634765625,
              -20.3034175184893
            ],
            [
              -69.927978515625,
              -20.3034175184893
            ],
            [
              -69.927978515625,
              -20.76638681251519
            ]
          ]
        ]
      }

    result = clip_polygon(tile, polygon)
    assert result == {"type": "Polygon", "coordinates": [[[-68.5711669921875, -23.79539759797873], [-66.7254638671875, -23.79539759797873], [-66.7254638671875, -22.61908160971607], [-68.5711669921875, -22.61908160971607], [-68.5711669921875, -23.79539759797873]]]} # noqa

    outside_result = clip_polygon(tile, polygon_outside)
    assert outside_result == polygon_outside
