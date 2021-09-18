import logging
import pathlib
import pytest

from photoheading.basemap import Basemap

DATA_FOLDER = pathlib.Path(__file__).parents[1] / 'data' / 'input' / 'basemaps'
IMAGE_PATH = DATA_FOLDER / 'School01.jpg'

@pytest.fixture
def victim():
    return Basemap(IMAGE_PATH, log_level=logging.DEBUG)

def test_bounds(victim):
    assert victim.bounds.left == 355511.7
