import unittest
import sys, os
import shutil
import json
import psycopg2

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Insanity for getting parent folder in path
from postgis2geojson import postgis2geojson
from shapefile2postgis import shapefile2postgis
OUTPUT_PATH = "/tiler-data/geojson/test_states.geojson"

class TestPostgis2Geojson(unittest.TestCase):

    def test_postgis2geojson_notable(self):
        with self.assertRaises(OSError):
            postgis2geojson("non_existant_table", self.DB_VARS , LAYER_CONFIG=False)

    def setUp(self):
        try:
            os.remove(OUTPUT_PATH)
        except OSError:
            pass

        try:
            self.DB_VARS = {
                "DB_HOST" : "localhost", # os.environ["DB_HOST"],
                "DB_NAME" : "gis", # os.environ["DB_NAME"],
                "DB_PORT" : 5432,
                "DB_USER" : "docker", # os.environ["DB_USER"],
                "DB_PASSWORD" : "docker" # os.environ["DB_PASSWORD"]
            }
            shapefile2postgis("/tiler-data/test-data/states/states.shp", "test_states", self.DB_VARS)
        except StandardError:
            self.fail("Couldn't setup the PostGIS table for conversion")

    def tearDown(self):
        try:
            print "\n Tearing tests down..."            
            os.remove("/tiler-data/geojson/non_existant_table.geojson")
            os.remove(OUTPUT_PATH)
        except OSError:
            pass

        try:
            conn_string = "host='{}' dbname='{}' user='{}' password='{}'".format(
                "localhost", # os.environ["DB_HOST"],
                "gis", # os.environ["DB_NAME"],
                "docker", # os.environ["DB_USER"],
                "docker", # os.environ["DB_PASSWORD"]
            )
            conn = psycopg2.connect(conn_string)
            cursor = conn.cursor()
            cursor.execute("DROP TABLE test_states")
            conn.commit()
            conn.close()
        except psycopg2.Error as e:
            print "\n Couldn't tear down PostGIS table test_states"
            print e.pgerror

if __name__ == '__main__':
    unittest.main()