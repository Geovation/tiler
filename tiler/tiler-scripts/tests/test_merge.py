import unittest
import sys, os
import shutil

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Insanity for getting parent folder in path
from tiler_helpers import absolute_file_paths
from tiler import tiles_from_config
from merge import merge_tile_directories, get_num_pbfs

class TestMerge(unittest.TestCase):

    def test_merge(self):
        config_path_1 = "/tiler-data/test-data/configs/merge1.tiler.json"
        self.assertTrue(os.path.isfile(config_path_1))
        tiles_from_config(config_path_1)
        output_path_1 = "/tiler-data/tiles/test_merge_1"
        self.assertTrue(os.path.isdir(output_path_1))
        num_pbfs_1 = get_num_pbfs(output_path_1)

        config_path_2 = "/tiler-data/test-data/configs/merge2.tiler.json"
        self.assertTrue(os.path.isfile(config_path_2))
        tiles_from_config(config_path_2)
        output_path_2 = "/tiler-data/tiles/test_merge_2"
        self.assertTrue(os.path.isdir(output_path_2))
        num_pbfs_2 = get_num_pbfs(output_path_2)

        total = num_pbfs_1 + num_pbfs_2

        merge_tile_directories(output_path_1, output_path_2, overwrite=False)
        num_pbfs_total = get_num_pbfs(output_path_2)
        self.assertEqual(total, num_pbfs_total)

    def tearDown(self):
        try:
            print "\n Tearing down the test..." 
            os.remove("/tiler-data/geojson/test_stations.geojson")           
            shutil.rmtree("/tiler-data/tiles/test_merge_1")
            shutil.rmtree("/tiler-data/tiles/test_merge_2")
        except OSError as os_err:
            print os_err  

if __name__ == '__main__':
    unittest.main()