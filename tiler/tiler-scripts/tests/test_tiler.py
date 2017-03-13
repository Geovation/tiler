import unittest
import sys, os
import shutil
import time
import psycopg2
import SocketServer
import threading
from handler import TestHandler

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Insanity for getting parent folder in path
from tiler import get_config, handle_config
from shapefile2postgis import shapefile2postgis

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
        self.assertFalse(os.path.isfile(MBTILES_DIR + "/8/0/0.pbf"))

    def test_tiler_geojson(self):
        config_path = "/tiler-data/test-data/configs/example2.tiler.json"
        self.assertTrue(os.path.isfile(config_path))

        handle_config(config_path)
        self.assertTrue(os.path.isdir(MBTILES_DIR))
        self.assertTrue(os.path.isfile(MBTILES_DIR + "/0/0/0.pbf"))
        self.assertTrue(os.path.isfile(MBTILES_DIR + "/7/20/45.pbf"))


    def test_tiler_postgis(self):
        config_path = "/tiler-data/test-data/configs/postgis.tiler.json"

        try:
            shapefile2postgis("/tiler-data/test-data/states/states.shp", "states")
        except OSError:
            self.fail("Couldn't setup the PostGIS table necessary for test")

        handle_config(config_path)
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
            cursor.execute("DROP TABLE states")
            conn = None
            cursor = None
        except OSError:
            self.fail("Couldn't tear down PostGIS table states")

    def test_tiler_url(self):
        config_path = "/tiler-data/test-data/configs/url.tiler.json"
        self.assertTrue(os.path.isfile(config_path))
        PORT = 8080
        SocketServer.TCPServer.allow_reuse_address = True
        server = SocketServer.TCPServer(("", PORT), TestHandler)
        thread = threading.Thread(target = server.serve_forever)
        thread.daemon = True
        thread.start()
        handle_config(config_path)
        server.shutdown()
        server.socket.close()
        self.assertTrue(os.path.isfile("/tiler-data/input/stations.zip"))
        self.assertTrue(os.path.isdir("/tiler-data/input/stations"))
        self.assertTrue(os.path.isdir(MBTILES_DIR))

    @classmethod
    def tearDown(cls):
        try:
            print "\n Tearing tests down..."
            os.remove("/tiler-data/input/stations.zip")
            shutil.rmtree("/tiler-data/input/stations")
            shutil.rmtree(MBTILES_DIR)
        except OSError as shutil_err:
            print shutil_err

if __name__ == '__main__':
    unittest.main()