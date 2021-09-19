"""Define the Photo class.

This is adapted from TerraPy's EXIF class.
"""

from PIL import Image
from PIL.ExifTags import GPSTAGS
from PIL.ExifTags import TAGS

from keenepyt.core.thing import Thing
from photoheading.exifcoords import EXIFCoords

class Photo(Thing):
    """Represents an image file with EXIF data."""

    exif = None
    path = None

    def __init__(self, path, helpers=None, **kwargs):
        """Initialize the photo.

        :param path: The path to a JPEG or TIFF file.
        :param helpers: The helpers object from any previously-initialized thing
        :param kwargs: Additional arguments to use when overriding this constructor
        """
        
        super().__init__(helpers, **kwargs)
        self.path = path
        image = Image.open(path)
        self.exif = image._getexif()

    def convert_coordinates(self, coords, epsg):
        if epsg is None:
            return coords

        import pycrs
        import pyproj
        
        wgs84 = pycrs.parse.from_epsg_code(4326).to_proj4()
        # output_crs = pycrs.parse.from_epsg_code(epsg).to_proj4()
        output_crs = '+proj=utm +zone=19 +ellps=GRS80 +units=m +no_defs'

        fromproj = pyproj.Proj(wgs84)
        toproj = pyproj.Proj(output_crs)

        # if len(coords) == 2:
        #     coords[2] = 0

        return pyproj.transform(fromproj, toproj, coords[0], coords[1])

    def get_coordinates(self, epsg=None):
        """
        If the EXIF header contains GNSS coordinates, then return them.
        Otherwise, return None.
        """

        if not self.exif:
            self.warning('No EXIF header in {}.'.format(self.path))
            return

        tag_dict = {}
        for numeric_key, val in self.exif.items():
            text_key = TAGS.get(numeric_key)
            if text_key:
                tag_dict[text_key] = val
        gps_info = tag_dict.get('GPSInfo')
        if not gps_info:
            self.warning('No coordinates in {}.'.format(self.path))
            return
        
        # Convert the coordinates to [X, Y, Z].
        coordobject = EXIFCoords(gps_info)
        coords = coordobject.coord_list

        # Reproject.
        return self.convert_coordinates(coords, epsg)
