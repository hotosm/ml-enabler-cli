from ml_enabler.utils import bbox_str_to_list, get_tile_center
import mercantile


def test_bbox_str_to_list():
    bbox_str = '12.45,75.23,11.67,76.89'
    assert(bbox_str_to_list(bbox_str)) == [12.45, 75.23, 11.67, 76.89]


def test_get_tile_center():
  tile = mercantile.Tile(39, 72, 7)
  assert(get_tile_center(tile)) == 'SRID=4326;POINT (-68.90625 -23.23509017801799)'