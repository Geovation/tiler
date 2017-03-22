# import unittest
# import sys 
# import os
# import shutil

# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Insanity for getting parent folder in path
# from update import *
# from shapefile2postgis import shapefile2postgis
# from tiler import *
# from tiler_helpers import absolute_file_paths
# import psycopg2
# from geojson_extent import geojson_extent


# UPDATE_NAME = "update_overwrite"
# UPDATE_DIR = "/tiler-data/tiles/" + UPDATE_NAME
# UPDATE_FILE = "/tiler-data/tiles/" + UPDATE_NAME + ".mbtiles"

# MBTILES_NAME = "update"
# MBTILES_DIR = "/tiler-data/tiles/" + MBTILES_NAME
# MBTILES_FILE = "/tiler-data/tiles/" + MBTILES_NAME + ".mbtiles"


# class TestUpdate(unittest.TestCase):
    

#     # def test_latlon_to_tile(self):

#     #     # THIS CHECKS IN TMS FORMAT: http://www.maptiler.org/google-maps-coordinates-tile-bounds-projection/

#     #     # THIS IS FOR ZOOM LEVEL 0
#     #     tile = lat_lon_to_tile(1.0, -1.0, 0)
#     #     self.assertEqual(tile[0], 0)
#     #     self.assertEqual(tile[1], 0)

#     #     tile = lat_lon_to_tile(1.0, 1.0, 0)
#     #     self.assertEqual(tile[0], 0)
#     #     self.assertEqual(tile[1], 0)

#     #     # THIS IS FOR ZOOM LEVEL 1
#     #     tile = lat_lon_to_tile(1.0, 1.0, 1)
#     #     self.assertEqual(tile[0], 1)
#     #     self.assertEqual(tile[1], 1)

#     #     tile = lat_lon_to_tile(-1.0, 1.0, 1)
#     #     self.assertEqual(tile[0], 1)
#     #     self.assertEqual(tile[1], 0)

#     #     tile = lat_lon_to_tile(1.0, -1.0, 1)
#     #     self.assertEqual(tile[0], 0)
#     #     self.assertEqual(tile[1], 1)

#     #     tile = lat_lon_to_tile(-1.0, -1.0, 1)
#     #     self.assertEqual(tile[0], 0)
#     #     self.assertEqual(tile[1], 0)

#     #     # tile = lat_lon_to_tile(67.0, 67.0, 2)
#     #     # self.assertEqual(tile[0], 2)
#     #     # self.assertEqual(tile[1], 3)

#     # def test_get_tile_bounding_box_one(self):

#     #     clip_lat = 85.05112877980659

#     #     bb = get_tile_bounding_box(10, 10, 20, 20, 0)
#     #     bb_min_y = bb[0][0]
#     #     bb_min_x = bb[0][1]

#     #     bb_max_y = bb[1][0]
#     #     bb_max_x = bb[1][1]

#     #     # Use almost equals because of library conversion errors (???)
#     #     self.assertAlmostEqual(bb_min_x, -180.0)
#     #     self.assertAlmostEqual(bb_max_x, 180.0)
#     #     self.assertAlmostEqual(bb_min_y, -clip_lat)
#     #     self.assertAlmostEqual(bb_max_y, clip_lat)

#     #     bb = get_tile_bounding_box(10, 10, 20, 20, 1)
#     #     bb_min_y = bb[0][0]
#     #     bb_min_x = bb[0][1]

#     #     bb_max_y = bb[1][0]
#     #     bb_max_x = bb[1][1]

#     #     # Use almost equals because of library conversion errors (???)
#     #     self.assertAlmostEqual(bb_min_x, 0.0)
#     #     self.assertAlmostEqual(bb_max_x, 180.0)
#     #     self.assertAlmostEqual(bb_min_y, 0.0)
#     #     self.assertAlmostEqual(bb_max_y, clip_lat)


#     # def test_get_tile_bounding_box_zoom_10(self):

#     #         clip_lat = 85.05112877980659

#     #         bb = get_tile_bounding_box(0.0001, 0.0001, 20, 20, 10)
#     #         bb_min_y = bb[0][0]
#     #         bb_min_x = bb[0][1]

#     #         # bb_max_y = bb[1][0]
#     #         # bb_max_x = bb[1][1]

#     #         # Use almost equals because of library conversion errors (???)
#     #         self.assertAlmostEqual(bb_min_x, 0.0)
#     #         self.assertAlmostEqual(bb_min_y, 0.0)

#     #         bb = get_tile_bounding_box(-20.0, -20.0, -0.0001, -0.0001, 10)

#     #         bb_max_y = bb[1][0]
#     #         bb_max_x = bb[1][1]

#     #         # Use almost equals because of library conversion errors (???)
#     #         self.assertAlmostEqual(bb_max_x, 0.0)
#     #         self.assertAlmostEqual(bb_max_y, 0.0)


#     # def test_get_tile_bounding_box(self):

#     #     zoom = 20 # 19 causes a failure?

#     #     for min_coord in range(-1, -84, -1):
#     #         for max_coord in range(1, 84):

#     #             #print min_coord, max_coord
#     #             min_x = float(min_coord)
#     #             min_y = float(min_coord)
#     #             max_x = float(max_coord)
#     #             max_y = float(max_coord)

#     #             bb = get_tile_bounding_box(min_x, min_y, max_x, max_y, zoom)

#     #             bb_min_y = bb[0][0]
#     #             bb_min_x = bb[0][1]

#     #             bb_max_y = bb[1][0]
#     #             bb_max_x = bb[1][1]

#     #             self.assertTrue(bb_min_x < bb_max_x)
#     #             self.assertTrue(bb_min_y < bb_max_y)

#     #             # Test that the cell boundaries are actually larger than
#     #             # the underlying data
#     #             self.assertTrue(bb_min_x <= min_x)
#     #             self.assertTrue(bb_min_y <= min_y)

#     #             self.assertTrue(bb_max_x >= max_x)
#     #             self.assertTrue(bb_max_y >= max_y)

#     def test_updating(self):

#         update_config = "/tiler-data/test-data/configs/update.tiler.json"
#         shapefile2postgis("/tiler-data/test-data/states/states.shp", "states")
  
#         tiles_from_config(update_config)
#         self.assertTrue(os.path.isfile("/tiler-data/geojson/states.geojson"))
#         self.assertTrue(os.path.isdir(MBTILES_DIR))
#         self.assertTrue(os.path.isfile(MBTILES_DIR + "/0/0/0.pbf"))

#         old_num_pbf = len([f for f in absolute_file_paths(MBTILES_DIR)])

#         layers = get_config(update_config)

#         layers["tileset"] = UPDATE_NAME
#         layers["data"]["stations"] = {
#             "minzoom" : 4,
#             "maxzoom" : 12
#         }

#         simplifcation = 0
#         shapefile2postgis("/tiler-data/test-data/us_stations/us_stations.shp", "stations")
#         # extent = geojson_extent("/tiler-data/geojson/stations.geojson")
#         # changes_bounding_box = extent
#         #changes_bounding_box = [-179.0, -89.0, 179.0, 89.0]
#         changes_bounding_box = [-77.2726, 38.7665, -76.842, 39.1199]
#         geometry_column = "wkb_geometry"
#         generate_changed_tiles(layers, simplifcation, changes_bounding_box, geometry_column)

#         self.assertTrue(os.path.isdir(MBTILES_DIR + "/4/"))
#         self.assertTrue(os.path.isdir(UPDATE_DIR + "/12/"))

#         update_tile_directories(MBTILES_DIR, UPDATE_DIR)
#         new_num_pbf = len([f for f in absolute_file_paths(UPDATE_DIR)])

#         print new_num_pbf, old_num_pbf
#         self.assertTrue(new_num_pbf > old_num_pbf)


#         try:
#             conn_string = "host='{}' dbname='{}' user='{}' password='{}'".format(
#                 os.environ["DB_HOST"],
#                 os.environ["DB_NAME"],
#                 os.environ["DB_USER"],
#                 os.environ["DB_PASSWORD"]
#             )
#             conn = psycopg2.connect(conn_string)
#             cursor = conn.cursor()
#             cursor.execute("DROP TABLE states")
#             cursor.execute("DROP TABLE stations")
#             conn = None
#             cursor = None

#         except OSError as err:
#             self.fail("Couldn't tear down PostGIS tables: " + err)


#     # def test_updating_clipping(self):
#     #     postgis_config = "/tiler-data/test-data/configs/update.tiler.json"
#     #     shapefile2postgis("/tiler-data/test-data/us_stations/us_stations_missing.shp", "missing")
#     #     shapefile2postgis("/tiler-data/test-data/us_stations/us_stations_extras.shp", "extras")

#     #     tiles_from_config(postgis_config)

#     #     name = "states"

#     #     self.assertTrue(os.path.isdir(MBTILES_DIR))
#     #     self.assertTrue(os.path.isfile(MBTILES_DIR + "/0/0/0.pbf"))
#     #     old_num_pbf = len([f for f in absolute_file_paths(MBTILES_DIR)])

#     #     layers = get_config(postgis_config)
#     #     layers["data"]["extras"] = {
#     #         "minzoom" : 5,
#     #         "maxzoom" : 16
#     #     }

#     #     simplifcation = 5
#     #     changes_bounding_box = geojson_extent("/tiler-data/geojson/us_stations_extras")
#     #     geometry_column = "wkb_geometry"
#     #     generate_changed_tiles(name, layers, simplifcation, changes_bounding_box, geometry_column)

#     #     new_num_pbf = len([f for f in absolute_file_paths(MBTILES_DIR)])
#     #     self.assertTrue(new_num_pbf > old_num_pbf)

#     #     try:
#     #         conn_string = "host='{}' dbname='{}' user='{}' password='{}'".format(
#     #             os.environ["DB_HOST"],
#     #             os.environ["DB_NAME"],
#     #             os.environ["DB_USER"],
#     #             os.environ["DB_PASSWORD"]
#     #         )
#     #         conn = psycopg2.connect(conn_string)
#     #         cursor = conn.cursor()
#     #         cursor.execute("DROP TABLE missing")
#     #         cursor.execute("DROP TABLE extras")
#     #         conn = None
#     #         cursor = None
#     #     except OSError as err:
#     #         self.fail("Couldn't tear down PostGIS tables: " + err)


#     def tearDown(self):
#         try:
#             print "\n Tearing tests down..."
#             shutil.rmtree(MBTILES_DIR)
#             # shutil.rmtree(UPDATE_DIR)
#             os.remove("/tiler-data/tiles/" + UPDATE_NAME)
#             os.remove("/tiler-data/geojson/states.geojson")
#         except OSError as shutil_err:
#             pass


# if __name__ == '__main__':
#     unittest.main()