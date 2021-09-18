import logging
import pytest

from photoheading.exifcoords import EXIFCoords

GPS_INFO = {0: (0, 0, 0, 0), 1: 'N', 2: ((44, 1), (48, 1), (57321, 10000)), 3: 'W', 4: ((73, 1), (3, 1), (12243, 10000)), 5: 0, 6: (309826, 1000)}
COORDS = [-73.05034008333332, 44.80159225, 309.826]

@pytest.fixture
def victim():
    return EXIFCoords(COORDS, log_level=logging.DEBUG)

def test_dd_to_dms(victim):
    result = victim.dd_to_dms(COORDS[0])
    print(result)
    
def test_dms_to_dd(victim):
    result = victim.dms_to_dd(GPS_INFO[2])
    print(result)
    
def test_tuple_to_float(victim):
    result = victim.tuple_to_float(GPS_INFO[2][2])
    print(result)
    
def test_init_from_coordlist(victim):
    assert victim.gps_info[3] == 'W'

def test_init_from_exif(victim):
    victim.init_from_exif(GPS_INFO)
    print(victim.coord_list)

if __name__ == '__main__':
    pytest.main([__file__])