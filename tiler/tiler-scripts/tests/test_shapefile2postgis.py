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
            shapefile2postgis("some/none/existant.file", "some_table")

    def test_shapefile2postgis(self):
        try:
            table = "states"
            shapefile2postgis("/tiler-data/test-data/states/states.shp", "states")
        except:
            self.fail("Shapefile not successfully added to table")

    def tearDown(self):

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