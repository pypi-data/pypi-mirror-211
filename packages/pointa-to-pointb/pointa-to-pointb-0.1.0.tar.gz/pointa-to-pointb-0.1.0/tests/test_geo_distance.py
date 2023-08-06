from pointa_to_pointb import geo_distance

def test_haversine():

    assert geo_distance.haversine(52.370216, 4.895168, 52.520008,
    13.404954) == 946.3876221719836
    assert geo_distance.haversine(52.370216, 4.895168, 52.520008,
    13.404954) == 945793.4375088713