"""Define the EXIFCoords class.

This is adapted from TerraPy's EXIFCoords class.
"""

import math
from keenepyt.core.thing import Thing

class EXIFCoords(Thing):
    """Stores and converts coordinates from an EXIF header."""
    
    gps_info = None
    coord_list = None
    
    def __init__(self, coords, helpers=None, **kwargs):
        """Initialize the coordinates.

        :param coords: The coordinates from a JPEG file's EXIF header.
        :param helpers: The helpers object from any previously-initialized thing
        :param kwargs: Additional arguments to use when overriding this constructor
        """
        
        super().__init__(helpers, **kwargs)
        coord_type = type(coords)
        if coord_type is list:
            self.init_from_coord_list(coords)
        elif coord_type is dict:
            self.init_from_exif(coords)
            
    def dd_to_dms(self, dd, seconds_multiplier=10000):
        """
        Given a floating-point number representing decimal degrees,
        convert it to a degrees-minutes-seconds tuple of integers.
        """
        
        abs_deg = math.fabs(dd)
        degrees_floor = math.floor(abs_deg)
        degrees_tuple = (int(degrees_floor), 1)
        
        dm = (abs_deg - degrees_floor) * 60
        minutes_floor = math.floor(dm)
        minutes_tuple = (int(minutes_floor), 1)
        
        ds = (dm - minutes_floor) * 60
        seconds_numerator = ds * seconds_multiplier
        seconds_tuple = (int(seconds_numerator), seconds_multiplier)
        
        return [degrees_tuple, minutes_tuple, seconds_tuple]
    
    def dms_to_dd(self, dms):
        """
        Given a tuple of degrees, minutes, and seconds in the EXIF format,
        convert it to decimal degrees.
        """

        degrees = self.tuple_to_float(dms[0])
        minutes = self.tuple_to_float(dms[1])
        seconds = self.tuple_to_float(dms[2])
        
        return degrees + (minutes / 60) + (seconds / 3600)
        
    def init_from_coord_list(self, coord_list):
        """
        Set the coordinates using an X, Y, Z list (longitude, latitude, and meters),
        and update the gps_info parameter using the EXIF format.
        """
        
        self.coord_list = coord_list
        return self.update_gps_info()
    
    def init_from_exif(self, gps_info):
        """
        Use the gps_info dictionary from an EXIF header to
        initialize the coordinates.
        """
        
        self.gps_info = gps_info
        return self.update_coord_list()
        
    def tuple_to_float(self, t):
        """
        An EXIF header stores a number two integers. Divide one by
        the other, and return the resulting non-integer.
        """ 
        
        if type(t) is not tuple:
            return float(t)
        numerator = float(t[0])
        denominator = float(t[1])
        return numerator / denominator
        
    def update_coord_list(self):
        """
        Assuming that the gps_info parameter has been set, convert
        it to an X, Y, Z list, and update the coord_list parameter.
        """
        
        if (self.gps_info is None) | (len(self.gps_info) == 0):
            self.raise_error('Please set the gps_info class parameter.')
        
        # Convert the latitude to decimal degrees.
        yref = self.gps_info[1]
        ydms = self.gps_info[2]
        ydd = self.dms_to_dd(ydms)
        if yref == 'S':
            ydd = -ydd
        
        # Convert the longitude to decimal degrees.
        xref = self.gps_info[3]
        xdms = self.gps_info[4]
        xdd = self.dms_to_dd(xdms)
        if xref == 'W':
            xdd = -xdd
        
        # Convert the altitude to meters.
        zm = self.tuple_to_float(self.gps_info[6])
        
        self.coord_list = [xdd, ydd, zm]
        
        return True
    
    def update_gps_info(self, seconds_multiplier=10000, altitude_multiplier=1000):
        """
        Assuming that the coord_list parameter has been set, convert
        it to the EXIF format, and update the gps_info parameter.
        """
        
        if self.coord_list is None:
            self.raise_error('Please set the coord_list class parameter.')
        
        longitude = self.coord_list[0]
        if longitude < 0:
            longitude_ref = 'W'
        else:
            longitude_ref = 'E'
        longitude_list = self.dd_to_dms(longitude, seconds_multiplier) 

        latitude = self.coord_list[1]
        if latitude < 0:
            latitude_ref = 'S'
        else:
            latitude_ref = 'N'
        latitude_list = self.dd_to_dms(latitude, seconds_multiplier) 

        big_z = self.coord_list[2] * altitude_multiplier
        altitude_tuple = (big_z, altitude_multiplier)
        
        self.gps_info = {
            0: (0, 0, 0, 0),
            1: latitude_ref,
            2: latitude_list,
            3: longitude_ref,
            4: longitude_list,
            5: 0,
            6: [altitude_tuple]
        }
        
        return True
        
