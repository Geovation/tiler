import unittest
import sys, os
import shutil
import time
import psycopg2
import SocketServer
import threading
from handler import TestHandler

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Insanity for getting parent folder in path
from tiler import get_config, tiles_from_config
from shapefile2postgis import shapefile2postgis

MBTILES_NAME = "test_states"
MBTILES_DIR = "/tiler-data/tiles/" + MBTILES_NAME

class TestTiler(unittest.TestCase):

    def test_get_config(self):
        config_path = "/tiler-data/test-data/configs/example.tiler.json"
        self.assertTrue(os.path.isfile(config_path))

        config = get_config(config_path)
        self.assertTrue(type(config) == dict)
        self.assertTrue(type(config["data"]) == dict)
        self.assertTrue(type(config["data"]["test_states"]) == dict)
        self.assertTrue(config["data"]["test_states"]["type"] == "shapefile")
        self.assertTrue(config["data"]["test_states"]["minzoom"] == 0)
        self.assertTrue(config["data"]["test_states"]["maxzoom"] == 4)
        self.assertTrue(config["data"]["test_states"]["maxzoom"] > config["data"]["test_states"]["minzoom"])


    def test_tiler(self):
        config_path = "/tiler-data/test-data/configs/example.tiler.json"
        self.assertTrue(os.path.isfile(config_path))

        tiles_from_config(config_path)
        self.assertTrue(os.path.isfile("/tiler-data/geojson/test_states.geojson"))
        self.assertTrue(os.path.isdir(MBTILES_DIR))
        self.assertTrue(os.path.isfile(MBTILES_DIR + "/0/0/0.pbf"))
        self.assertFalse(os.path.isfile(MBTILES_DIR + "/5/0/0.pbf"))
        self.assertFalse(os.path.isfile(MBTILES_DIR + "/8/0/0.pbf"))

    def test_tiler_geojson(self):
        config_path = "/tiler-data/test-data/configs/example2.tiler.json"
        self.assertTrue(os.path.isfile(config_path))

        tiles_from_config(config_path)
        self.assertTrue(os.path.isdir(MBTILES_DIR))
        self.assertTrue(os.path.isfile(MBTILES_DIR + "/0/0/0.pbf"))
        self.assertTrue(os.path.isfile(MBTILES_DIR + "/7/20/45.pbf"))

    def test_tiler_gml(self):
        config_path = "/tiler-data/test-data/configs/gml.tiler.json"
        self.assertTrue(os.path.isfile(config_path))

        tiles_from_config(config_path)
        self.assertTrue(os.path.isdir(MBTILES_DIR))
        self.assertTrue(os.path.isfile(MBTILES_DIR + "/0/0/0.pbf"))
    
    def test_tiler_postgis(self):
        config_path = "/tiler-data/test-data/configs/postgis.tiler.json"
        DB_VARS = {
            "DB_HOST" : "localhost", # os.environ["DB_HOST"],
            "DB_NAME" : "gis", # os.environ["DB_NAME"],
            "DB_PORT" : 5432,
            "DB_USER" : "docker", # os.environ["DB_USER"],
            "DB_PASSWORD" : "docker" # os.environ["DB_PASSWORD"]
        }
        try:
            shapefile2postgis("/tiler-data/test-data/states/states.shp", "test_states", DB_VARS)
        except OSError:
            self.fail("Couldn't setup the PostGIS table necessary for test")

        tiles_from_config(config_path)
        self.assertTrue(os.path.isdir(MBTILES_DIR))
        self.assertTrue(os.path.isfile(MBTILES_DIR + "/0/0/0.pbf"))

        try:
            conn_string = "host='{}' dbname='{}' user='{}' password='{}'".format(
                os.environ["DB_HOST"],
                os.environ["DB_NAME"],
                os.environ["DB_USER"],
                os.environ["DB_PASSWORD"]
            )
            conn = psycopg2.connect(conn_string)
            cursor = conn.cursor()
            cursor.execute("DROP TABLE test_states")
            conn.commit()
            conn.close()
        except psycopg2.Error as e:
            print "\n Couldn't tear down PostGIS table test_states"
            print e.pgerror

    def test_tiler_shapefile_database(self):
        config_path = "/tiler-data/test-data/configs/example3.tiler.json"
        self.assertTrue(os.path.isfile(config_path))

        tiles_from_config(config_path)
        self.assertTrue(os.path.isdir(MBTILES_DIR))
        self.assertTrue(os.path.isfile(MBTILES_DIR + "/0/0/0.pbf"))
        self.assertFalse(os.path.isfile(MBTILES_DIR + "/5/0/0.pbf"))
        self.assertFalse(os.path.isfile(MBTILES_DIR + "/8/0/0.pbf"))

        try:
            conn_string = "host='{}' dbname='{}' user='{}' password='{}'".format(
                os.environ["DB_HOST"],
                os.environ["DB_NAME"],
                os.environ["DB_USER"],
                os.environ["DB_PASSWORD"]
            )
            conn = psycopg2.connect(conn_string)
            cursor = conn.cursor()
            cursor.execute("DROP TABLE test_states")
            conn.commit()
            conn.close()
        except psycopg2.Error as e:
            print "\n Couldn't tear down PostGIS table test_states"
            print e.pgerror

    def test_tiler_url(self):
        config_path = "/tiler-data/test-data/configs/url.tiler.json"
        self.assertTrue(os.path.isfile(config_path))
        PORT = 8080
        SocketServer.TCPServer.allow_reuse_address = True
        server = SocketServer.TCPServer(("", PORT), TestHandler)
        thread = threading.Thread(target = server.serve_forever)
        thread.daemon = True
        thread.start()
        tiles_from_config(config_path)
        server.shutdown()
        server.socket.close()
        self.assertTrue(os.path.isfile("/tiler-data/input/stations.zip"))
        self.assertTrue(os.path.isdir("/tiler-data/input/stations"))
        self.assertTrue(os.path.isfile("/tiler-data/input/stations/stations.shp"))
        self.assertTrue(os.path.isfile("/tiler-data/input/states.geojson"))
        self.assertTrue(os.path.isdir(MBTILES_DIR))

    def tearDown(self):
        try:
            print "\n Tearing tests down..."
            shutil.rmtree(MBTILES_DIR)
            os.remove("/tiler-data/geojson/test_states.geojson")    
        except OSError:
            pass

        try:
            print "\n Tearing test_tiler_url down..."
            os.remove("/tiler-data/geojson/test_stations.geojson")
            os.remove("/tiler-data/input/states.geojson")
            os.remove("/tiler-data/input/stations.zip")
            shutil.rmtree("/tiler-data/input/stations")
        except OSError as os_err:
            pass

if __name__ == '__main__':
    unittest.main()