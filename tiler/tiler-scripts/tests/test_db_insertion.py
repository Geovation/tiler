import unittest
import sys, os
import shutil
import json
import psycopg2

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Insanity for getting parent folder in path
from shapefile2postgis import shapefile2postgis
from postgis2geojson import postgis2geojson
from tiler import tiles_from_config

MBTILES_NAME = "test_states"
MBTILES_DIR = "/tiler-data/tiles/" + MBTILES_NAME
OUTPUT_PATH = "/tiler-data/geojson/test_states.geojson"

class TestdbInsertion(unittest.TestCase):
    """Tests if data get inserted correctly into database"""
    
    def test_db_insertion(self):
        """Does states.shp data get inserted correctly into database?"""     

        config_path = "/tiler-data/test-data/configs/insertDatabase.tiler.json"
        self.assertTrue(os.path.isfile(config_path))

        tiles_from_config(config_path)
        self.assertTrue(os.path.isfile("/tiler-data/geojson/test_states.geojson"))
        self.assertTrue(os.path.isdir(MBTILES_DIR))
        self.assertTrue(os.path.isfile(MBTILES_DIR + "/0/0/0.pbf"))
        self.assertFalse(os.path.isfile(MBTILES_DIR + "/5/0/0.pbf"))
        self.assertFalse(os.path.isfile(MBTILES_DIR + "/8/0/0.pbf"))

        try:
            conn = self.get_connection()
            cursor = conn.cursor()
        except:
            self.fail("Couldn't connect to the database")

        try:
            cursor.execute("SELECT * FROM test_states")
            records = cursor.fetchall()
            conn.close()
            self.assertTrue(len(records) == 51)
            self.assertEqual(records[0][2], "Hawaii")
            self.assertEqual(records[50][2], "Alaska")
        except:
            self.fail("Table states contents not successfully fetched")

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
            print "\n Tearing down the test..."
            os.remove(OUTPUT_PATH)
            shutil.rmtree(MBTILES_DIR)
        except OSError as os_err:
            print os_err            

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