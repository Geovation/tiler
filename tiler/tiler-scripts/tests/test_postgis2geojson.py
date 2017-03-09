import unittest
import sys, os
import shutil
import json
import psycopg2

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Insanity for getting parent folder in path
from postgis2geojson import postgis2geojson
from shapefile2postgis import shapefile2postgis
OUTPUT_PATH = "/tiler-data/geojson/states.geojson"

class TestPostgis2Geojson(unittest.TestCase):

    def test_postgis2geojson_notable(self):
        with self.assertRaises(OSError):
            postgis2geojson("non_existant_table", os.environ, LAYER_CONFIG=False)

    def setUp(self):
        try:
            os.remove(OUTPUT_PATH)
        except OSError:
            pass

        try:
            shapefile2postgis("/tiler-data/test-data/states/states.shp", "states")
        except OSError:
            self.fail("Couldn't setup the PostGIS table for conversion")

    def tearDown(self):
        try:
            print "\n Tearing tests down..."
            os.remove(OUTPUT_PATH)
        except OSError:
            pass

        try:
            conn_string = "host='{}' dbname='{}' user='{}' password='{}'".format(
                os.environ["DB_HOST"],
                os.environ["DB_NAME"],
                os.environ["DB_USER"],
                os.environ["DB_PASSWORD"]
            )
            conn = psycopg2.connect(conn_string)
            cursor = conn.cursor()
            cursor.execute("DROP TABLE states")
            conn = None
            cursor = None
        except OSError:
            self.fail("Couldn't tear down PostGIS table states")


if __name__ == '__main__':
    unittest.main()