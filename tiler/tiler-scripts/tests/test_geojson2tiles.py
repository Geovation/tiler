import unittest
import sys, os
import shutil
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Insanity for getting parent folder in path
from geojson2tiles import *


MBTILES_NAME = "states"
MBTILES_DIR = "/tiler-data/tiles/" + MBTILES_NAME
MBTILES_FILE = "/tiler-data/tiles/" + MBTILES_NAME + ".mbtiles"

UPDATE_MBTILES_DIR = "/tiler-data/updates/" + MBTILES_NAME
UPDATE_MBTILES_FILE = "/tiler-data/updates/" + MBTILES_FILE + ".mbtiles"


class TestGeojson2Tiles(unittest.TestCase):

    def test_create_mbtiles(self):
        GEOJSON_FILES = ["/tiler-data/test-data/"+ MBTILES_NAME +".geojson"]
        MIN_ZOOM = 0
        MAX_ZOOM = 4
        SIMPLIFICATION = 1

        self.assertTrue(os.path.isfile(GEOJSON_FILES[0]))

        create_mbtiles(GEOJSON_FILES, MBTILES_NAME, MIN_ZOOM, MAX_ZOOM, SIMPLIFICATION)
        self.assertTrue(os.path.isfile(MBTILES_FILE))

    def test_extract_pbf(self):

        extract_pbf(MBTILES_NAME, False)
        self.assertTrue(os.path.isdir(MBTILES_DIR))
        self.assertTrue(os.path.isfile(MBTILES_DIR + "/0/0/0.pbf"))

    def test_decompress_pbf(self):
 
        extract_pbf(MBTILES_NAME, False)
        self.assertTrue(os.path.isdir(MBTILES_DIR))
        self.assertTrue(os.path.isfile(MBTILES_DIR + "/0/0/0.pbf"))

        decompress_pbf(MBTILES_NAME, False)
        gz_magic = "\x1f\x8b\x08"
        with open(MBTILES_DIR + "/0/0/0.pbf") as f:
            file_start = f.read(len(gz_magic))
            is_gzipped = file_start.startswith(gz_magic)
            self.assertFalse(is_gzipped)

    def test_extract_pbf_update(self):

        extract_pbf(MBTILES_NAME, True)
        self.assertTrue(os.path.isdir(UPDATE_MBTILES_DIR))
        self.assertTrue(os.path.isfile(UPDATE_MBTILES_DIR + "/0/0/0.pbf"))

    def test_decompress_pbf_update(self):

        # Setup the tiles to be overwritten
        extract_pbf(MBTILES_NAME, False)
        decompress_pbf(MBTILES_NAME, False)

        last_modified = os.stat(MBTILES_DIR + "/0/0/0.pbf").st_mtime

        extract_pbf(MBTILES_NAME, True)
        self.assertTrue(os.path.isdir(UPDATE_MBTILES_DIR))
        self.assertTrue(os.path.isfile(UPDATE_MBTILES_DIR + "/0/0/0.pbf"))

        decompress_pbf(MBTILES_NAME, True)
        
        # Modified times are at most granular in seconds, so we need to wait for changes 
        time.sleep(5)
        modified = os.stat(MBTILES_DIR + "/0/0/0.pbf").st_mtime
        self.assertNotEqual(modified, last_modified)

        gz_magic = "\x1f\x8b\x08"
        with open(MBTILES_DIR + "/0/0/0.pbf") as f:
            file_start = f.read(len(gz_magic))
            is_gzipped = file_start.startswith(gz_magic)
            self.assertFalse(is_gzipped)



    @classmethod
    def tearDown(cls):
        try:
            print "\n Tearing tests down..."
            shutil.rmtree(MBTILES_DIR)
            shutil.rmtree(UPDATE_MBTILES_DIR)
        except OSError as shutil_err:
            print shutil_err

if __name__ == '__main__':
    unittest.main()