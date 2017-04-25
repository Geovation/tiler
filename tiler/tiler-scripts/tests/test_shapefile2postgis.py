import unittest
import sys, os
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
            table = "test_states"
            shapefile2postgis("/tiler-data/test-data/states/states.shp", table, self.DB_VARS)
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM test_states")
            records = cursor.fetchall()
            conn.close()
            self.assertTrue(len(records) == 51)
            self.assertEqual(records[0][2], "Hawaii")
            self.assertEqual(records[50][2], "Alaska")
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
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("DROP TABLE test_states")
            conn.commit()
            conn.close()
        except psycopg2.Error as e:
            print "\n Couldn't tear down PostGIS table test_states"
            print e.pgerror

    def get_connection(self):
        conn_string = "host='{}' dbname='{}' user='{}' password='{}'".format(
                "localhost", # os.environ["DB_HOST"],
                "gis", # os.environ["DB_NAME"],
                "docker", # os.environ["DB_USER"],
                "docker", # os.environ["DB_PASSWORD"]
            )
        conn = psycopg2.connect(conn_string)
        return conn

if __name__ == '__main__':
    unittest.main()