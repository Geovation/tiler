import unittest
import sys, os
import shutil

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Insanity for getting parent folder in path
from validate_geojson import *

class TestValidateGeojson(unittest.TestCase):

    def test_create_mbtiles(self):
        GEOJSON_FILE = "/tiler-data/test-data/states.geojson"
        is_valid = validate_geojson(GEOJSON_FILE)

        self.assertTrue(is_valid)

if __name__ == '__main__':
    unittest.main()