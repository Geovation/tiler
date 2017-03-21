import unittest
import sys 
import os
import shutil

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Insanity for getting parent folder in path
from update import *
from shapefile2postgis import shapefile2postgis
from tiler import *
from tiler_helpers import absolute_file_paths
import psycopg2

MBTILES_NAME = "states"
MBTILES_DIR = "/tiler-data/tiles/" + MBTILES_NAME
MBTILES_FILE = "/tiler-data/tiles/" + MBTILES_NAME + ".mbtiles"


class TestUpdate(unittest.TestCase):
    

    def test_latlon_to_tile(self):

        # THIS CHECKS IN TMS FORMAT: http://www.maptiler.org/google-maps-coordinates-tile-bounds-projection/

        # THIS IS FOR ZOOM LEVEL 0
        tile = lat_lon_to_tile(1.0, -1.0, 0)
        self.assertEqual(tile[0], 0)
        self.assertEqual(tile[1], 0)

        tile = lat_lon_to_tile(1.0, 1.0, 0)
        self.assertEqual(tile[0], 0)
        self.assertEqual(tile[1], 0)

        # THIS IS FOR ZOOM LEVEL 1
        tile = lat_lon_to_tile(1.0, 1.0, 1)
        self.assertEqual(tile[0], 1)
        self.assertEqual(tile[1], 1)

        tile = lat_lon_to_tile(-1.0, 1.0, 1)
        self.assertEqual(tile[0], 1)
        self.assertEqual(tile[1], 0)

        tile = lat_lon_to_tile(1.0, -1.0, 1)
        self.assertEqual(tile[0], 0)
        self.assertEqual(tile[1], 1)

        tile = lat_lon_to_tile(-1.0, -1.0, 1)
        self.assertEqual(tile[0], 0)
        self.assertEqual(tile[1], 0)

        # tile = lat_lon_to_tile(67.0, 67.0, 2)
        # self.assertEqual(tile[0], 2)
        # self.assertEqual(tile[1], 3)

    def test_get_tile_bounding_box_one(self):

        clip_lat = 85.05112877980659

        bb = get_tile_bounding_box(10, 10, 20, 20, 0)
        bb_min_y = bb[0][0]
        bb_min_x = bb[0][1]

        bb_max_y = bb[1][0]
        bb_max_x = bb[1][1]

        # Use almost equals because of library conversion errors (???)
        self.assertAlmostEqual(bb_min_x, -180.0)
        self.assertAlmostEqual(bb_max_x, 180.0)
        self.assertAlmostEqual(bb_min_y, -clip_lat)
        self.assertAlmostEqual(bb_max_y, clip_lat)

        bb = get_tile_bounding_box(10, 10, 20, 20, 1)
        bb_min_y = bb[0][0]
        bb_min_x = bb[0][1]

        bb_max_y = bb[1][0]
        bb_max_x = bb[1][1]

        # Use almost equals because of library conversion errors (???)
        self.assertAlmostEqual(bb_min_x, 0.0)
        self.assertAlmostEqual(bb_max_x, 180.0)
        self.assertAlmostEqual(bb_min_y, 0.0)
        self.assertAlmostEqual(bb_max_y, clip_lat)


    def test_get_tile_bounding_box_zoom_10(self):

            clip_lat = 85.05112877980659

            bb = get_tile_bounding_box(0.0001, 0.0001, 20, 20, 10)
            bb_min_y = bb[0][0]
            bb_min_x = bb[0][1]

            # bb_max_y = bb[1][0]
            # bb_max_x = bb[1][1]

            # Use almost equals because of library conversion errors (???)
            self.assertAlmostEqual(bb_min_x, 0.0)
            self.assertAlmostEqual(bb_min_y, 0.0)

            bb = get_tile_bounding_box(-20.0, -20.0, -0.0001, -0.0001, 10)

            bb_max_y = bb[1][0]
            bb_max_x = bb[1][1]

            # Use almost equals because of library conversion errors (???)
            self.assertAlmostEqual(bb_max_x, 0.0)
            self.assertAlmostEqual(bb_max_y, 0.0)


    def test_get_tile_bounding_box(self):

        zoom = 20 # 19 causes a failure?

        for min_coord in range(-1, -84, -1):
            for max_coord in range(1, 84):

                #print min_coord, max_coord
                min_x = float(min_coord)
                min_y = float(min_coord)
                max_x = float(max_coord)
                max_y = float(max_coord)

                bb = get_tile_bounding_box(min_x, min_y, max_x, max_y, zoom)

                bb_min_y = bb[0][0]
                bb_min_x = bb[0][1]

                bb_max_y = bb[1][0]
                bb_max_x = bb[1][1]

                self.assertTrue(bb_min_x < bb_max_x)
                self.assertTrue(bb_min_y < bb_max_y)

                # Test that the cell boundaries are actually larger than
                # the underlying data
                self.assertTrue(bb_min_x <= min_x)
                self.assertTrue(bb_min_y <= min_y)

                self.assertTrue(bb_max_x >= max_x)
                self.assertTrue(bb_max_y >= max_y)


    def test_updating(self):

        postgis_config = "/tiler-data/test-data/configs/postgis.tiler.json"
        shapefile2postgis("/tiler-data/test-data/states/states.shp", "states")
        shapefile2postgis("/tiler-data/test-data/us_stations/us_stations.shp", "stations")
        handle_config(postgis_config)

        name = "states"

        self.assertTrue(os.path.isdir(MBTILES_DIR))
        self.assertTrue(os.path.isfile(MBTILES_DIR + "/0/0/0.pbf"))
        old_num_pbf = len([f for f in absolute_file_paths(MBTILES_DIR)])

        layers = get_config(postgis_config)
        layers["data"]["stations"] = {
            "minzoom" : 4,
            "maxzoom" : 12
        }
        simplifcation = 5
        changes_bounding_box = [-77.2726, 38.7665, -76.842, 39.1199]
        geometry_column = "wkb_geometry"
        generate_changed_tiles(name, layers, simplifcation, changes_bounding_box, geometry_column)

        new_num_pbf = len([f for f in absolute_file_paths(MBTILES_DIR)])
        self.assertTrue(new_num_pbf > old_num_pbf)
        self.assertTrue(os.path.isdir(MBTILES_DIR + "/12/"))

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
            cursor.execute("DROP TABLE stations")
            conn = None
            cursor = None
        except OSError as err:
            self.fail("Couldn't tear down PostGIS tables: " + err)


    # def test_updating_clipping(self):
        # postgis_config = "/tiler-data/test-data/configs/update.tiler.json"
        # shapefile2postgis("/tiler-data/test-data/us_stations/us_stations_missing.shp", "missing")
        # shapefile2postgis("/tiler-data/test-data/us_stations/us_stations_extras.shp", "extras")

        # handle_config(postgis_config)

        # name = "states"

        # self.assertTrue(os.path.isdir(MBTILES_DIR))
        # self.assertTrue(os.path.isfile(MBTILES_DIR + "/0/0/0.pbf"))
        # old_num_pbf = len([f for f in absolute_file_paths(MBTILES_DIR)])

        # layers = get_config(postgis_config)
        # layers["data"]["extras"] = {
        #     "minzoom" : 5,
        #     "maxzoom" : 16
        # }
        # simplifcation = 5
        # changes_bounding_box = geojson_extent("/tiler-data/geojson/us_stations_extras")
        # geometry_column = "wkb_geometry"
        # generate_changed_tiles(name, layers, simplifcation, changes_bounding_box, geometry_column)

        # new_num_pbf = len([f for f in absolute_file_paths(MBTILES_DIR)])
        # self.assertTrue(new_num_pbf > old_num_pbf)
        # self.assertTrue(os.path.isdir(MBTILES_DIR + "/12/"))

        # try:
        #     conn_string = "host='{}' dbname='{}' user='{}' password='{}'".format(
        #         os.environ["DB_HOST"],
        #         os.environ["DB_NAME"],
        #         os.environ["DB_USER"],
        #         os.environ["DB_PASSWORD"]
        #     )
        #     conn = psycopg2.connect(conn_string)
        #     cursor = conn.cursor()
        #     cursor.execute("DROP TABLE states")
        #     cursor.execute("DROP TABLE stations")
        #     conn = None
        #     cursor = None
        # except OSError as err:
        #     self.fail("Couldn't tear down PostGIS tables: " + err)


    def tearDown(self):
        try:
            print "\n Tearing tests down..."
            shutil.rmtree(MBTILES_DIR)
        except OSError as shutil_err:
            pass


if __name__ == '__main__':
    unittest.main()