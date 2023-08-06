from pointa_to_pointb import bbox_distance

def test_bbox_distance():

    bbox1 = (20, 21, 25, 18)
    bbox2 = (55, 55, 100, 10)

    assert bbox_distance.manhanttan_distance(bbox1, bbox2) == 64
    assert bbox_distance.gap_distance(bbox1, bbox2) == 30