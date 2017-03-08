import unittest
import sys, os
import shutil

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Insanity for getting parent folder in path
from tiler import *

MBTILES_NAME = "states"
MBTILES_DIR = "/tiler-data/tiles/" + MBTILES_NAME
MBTILES_FILE = "/tiler-data/tiles/" + MBTILES_NAME + ".mbtiles"

class TestTiler(unittest.TestCase):

    def test_get_config(self):
        config_path = "/tiler-data/test-data/configs/example.tiler.json"
        self.assertTrue(os.path.isfile(config_path))

        config = get_config(config_path)
        self.assertTrue(type(config) == dict)
        self.assertTrue(type(config["data"]) == dict)
        self.assertTrue(type(config["data"]["states"]) == dict)
        self.assertTrue(config["data"]["states"]["type"] == "shapefile")
        self.assertTrue(config["data"]["states"]["minzoom"] == 0)
        self.assertTrue(config["data"]["states"]["maxzoom"] == 4)
        self.assertTrue(config["data"]["states"]["maxzoom"] > config["data"]["states"]["minzoom"])

    def test_tiler(self):
        config_path = "/tiler-data/test-data/configs/example.tiler.json"
        self.assertTrue(os.path.isfile(config_path))
        
        handle_config(config_path)
        self.assertTrue(os.path.isdir(MBTILES_DIR))
        self.assertTrue(os.path.isfile(MBTILES_DIR + "/0/0/0.pbf"))
        self.assertFalse(os.path.isfile(MBTILES_DIR + "/5/0/0.pbf"))

    @classmethod
    def tearDown(cls):
        try:
            print "\n Tearing tests down..."
            shutil.rmtree(MBTILES_DIR)
        except OSError as shutil_err:
            print shutil_err

if __name__ == '__main__':
    unittest.main()