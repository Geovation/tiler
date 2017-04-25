import unittest
import sys, os
import shutil
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Insanity for getting parent folder in path
from gml2geojson import *

INPUT_PATH = "/tiler-data/test-data/states.gmlx"
OUTPUT_NAME = "test_states"
OUTPUT_PATH = "/tiler-data/geojson/{}.geojson".format(OUTPUT_NAME)

class TestGML2Geojson(unittest.TestCase):

    def test_wrongpath_gml2geojson(self):
        with self.assertRaises(OSError):
            gml2geojson("/some/wrong/path", "wrongpath"), 
        
    def test_gml2geojson(self):
        gml2geojson(INPUT_PATH, OUTPUT_NAME)
        self.assertTrue(os.path.isfile(OUTPUT_PATH))
        
        with open(OUTPUT_PATH) as data_file:
            geojson = json.load(data_file)
            self.assertIsInstance(geojson, dict)
            self.assertTrue(len(geojson["features"]) == 51)

    def test_gml2geojson_with_config(self):
        
        LAYER_CONFIG = {
            "layer" : "test_states",
            "maxzoom" : 4,
            "minzoom" : 0
        }

        gml2geojson(INPUT_PATH, OUTPUT_NAME, LAYER_CONFIG)
        self.assertTrue(os.path.isfile(OUTPUT_PATH))

        with open(OUTPUT_PATH) as data_file:
            geojson = json.load(data_file)
            self.assertIsInstance(geojson, dict)
            self.assertTrue(len(geojson["features"]) == 51)
            for feature in geojson["features"]:
                print feature
                self.assertIsInstance(feature["tippecanoe"], dict)
                self.assertEqual(feature["tippecanoe"]["layer"], "test_states")
                self.assertEqual(feature["tippecanoe"]["maxzoom"], 4)
                self.assertEqual(feature["tippecanoe"]["minzoom"], 0)

    @classmethod
    def tearDown(cls):
        try:
            print "\n Tearing tests down..."
            os.remove(OUTPUT_PATH)
        except OSError as os_err:
            print os_err

if __name__ == '__main__':
    unittest.main()