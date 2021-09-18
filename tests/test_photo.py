import logging
import pathlib
import pytest

from photoheading.photo import Photo

COORDS = [-73.05034008333332, 44.80159225, 309.826]

IMAGE_TIME = '2019-09-12 13:59:05'
exifversion = '0230'

PATH = pathlib.Path(__file__).parents[1] / 'data' / 'input' / 'photos01' / 'DJI_0235.jpg'

@pytest.fixture
def victim():
    return Photo(PATH, log_level=logging.DEBUG)

def test_get_coordinates(victim):
    result = victim.get_coordinates()
    assert result[0] == -70.78108716666667

    result = victim.get_coordinates(6348)
    assert result[0] == 5698047.219041451
