import unittest
import sys, os
import shutil
import json
import psycopg2

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Insanity for getting parent folder in path
from shapefile2postgis import shapefile2postgis

class TestPostgis2Geojson(unittest.TestCase):

    def test_shapefile2postgis_nofile(self):
        with self.assertRaises(OSError):
            shapefile2postgis("some/none/existant.file", "some_table", self.DB_VARS)

    def test_shapefile2postgis(self):
        try:
            table = "states"

            shapefile2postgis("/tiler-data/test-data/states/states.shp", "states", self.DB_VARS)
            cursor = self.get_cursor()
            cursor.execute("SELECT * FROM states")
            records = cursor.fetchall()
            # print records  # See the records if you want to do a sanity check
            self.assertTrue(len(records) > 0)
        except:
            self.fail("Shapefile not successfully added to table")

    def setUp(self):
        self.DB_VARS = {
            "DB_HOST" : "localhost", # os.environ["DB_HOST"],
            "DB_NAME" : "gis", # os.environ["DB_NAME"],
            "DB_PORT" : 5432,
            "DB_USER" : "docker", # os.environ["DB_USER"],
            "DB_PASSWORD" : "docker" # os.environ["DB_PASSWORD"]
        }

    def tearDown(self):

        try:
            print "\n Tearing down database..."
            cursor = self.get_cursor()
            cursor.execute("DROP TABLE states")
            cursor = None
        except OSError:
            self.fail("Couldn't tear down PostGIS table states")

    
    def get_cursor(self):
        conn_string = "host='{}' dbname='{}' user='{}' password='{}'".format(
                "localhost", # os.environ["DB_HOST"],
                "gis", # os.environ["DB_NAME"],
                "docker", # os.environ["DB_USER"],
                "docker", # os.environ["DB_PASSWORD"]
            )
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        return cursor


if __name__ == '__main__':
    unittest.main()