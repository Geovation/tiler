import unittest
import sys, os
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Insanity for getting parent folder in path
from shapefile2geojson import *

INPUT_PATH = "/tiler-data/test-data/states/states.shp"
OUTPUT_NAME = "test_states"
OUTPUT_PATH = "/tiler-data/geojson/{}.geojson".format(OUTPUT_NAME)

class TestShapefile2Geojson(unittest.TestCase):

    def test_wrongpath_shapefile2geojson(self):
        with self.assertRaises(OSError):
            shapefile2geojson("/some/wrong/path", "wrongpath")
        
    def test_shapefile2geojson(self):
        shapefile2geojson(INPUT_PATH, OUTPUT_NAME)
        self.assertTrue(os.path.isfile(OUTPUT_PATH))
        
        with open(OUTPUT_PATH) as data_file:
            geojson = json.load(data_file)
            self.assertIsInstance(geojson, dict)
            self.assertTrue(len(geojson["features"]) == 51)

    def test_shapefile2geojson_with_config(self):
        
        LAYER_CONFIG = {
            "layer" : "test_states",
            "maxzoom" : 4,
            "minzoom" : 0
        }
        
        shapefile2geojson(INPUT_PATH, OUTPUT_NAME, LAYER_CONFIG)
        self.assertTrue(os.path.isfile(OUTPUT_PATH))
        
        with open(OUTPUT_PATH) as data_file:
            geojson = json.load(data_file)
            self.assertIsInstance(geojson, dict)
            self.assertTrue(len(geojson["features"]) == 51)
            for feature in geojson["features"]:
                self.assertIsInstance(feature["tippecanoe"], dict)
                self.assertEqual(feature["tippecanoe"]["layer"], "test_states")
                self.assertEqual(feature["tippecanoe"]["maxzoom"], 4)
                self.assertEqual(feature["tippecanoe"]["minzoom"], 0)

    @classmethod
    def tearDown(cls):
        try:
            print "\n Tearing tests down..."
            os.remove(OUTPUT_PATH)
        except OSError:
            pass

if __name__ == '__main__':
    unittest.main()