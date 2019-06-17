from ml_enabler.utils import bbox_str_to_list

def test_bbox_str_to_list():
    bbox_str = '12.45,75.23,11.67,76.89'
    assert(bbox_str_to_list(bbox_str)) == [12.45, 75.23, 11.67, 76.89]

