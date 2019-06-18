from ml_enabler.utils import bbox_str_to_list, get_tile_center, bbox_to_polygon_wkt
import mercantile


def test_bbox_str_to_list():
    bbox_str = '12.45,75.23,11.67,76.89'
    assert(bbox_str_to_list(bbox_str)) == [12.45, 75.23, 11.67, 76.89]


def test_get_tile_center():
    tile = mercantile.Tile(39, 72, 7)
    assert(get_tile_center(tile)) == 'SRID=4326;POINT (-68.90625 -23.23509017801799)'


def test_bbox_to_polygon_wkt():
    tile = mercantile.Tile(39, 72, 7)
    bounds = mercantile.bounds(tile)
    assert bbox_to_polygon_wkt(list(bounds)) == 'POLYGON ((-67.5 -24.5271348225978, -67.5 -21.94304553343818, -70.3125 -21.94304553343818, -70.3125 -24.5271348225978, -67.5 -24.5271348225978))'
