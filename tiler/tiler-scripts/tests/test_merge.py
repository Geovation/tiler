import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Insanity for getting parent folder in path
from tiler_helpers import absolute_file_paths
from tiler import tiles_from_config
from merge import merge_tile_directories, get_num_pbfs
import unittest


class TestMerge(unittest.TestCase):

    def test_merge(self):
        config_path_1 = "/tiler-data/test-data/configs/merge1.tiler.json"
        self.assertTrue(os.path.isfile(config_path_1))
        tiles_from_config(config_path_1)
        output_path_1 = "/tiler-data/tiles/merge_1"
        self.assertTrue(os.path.isdir(output_path_1))
        num_pbfs_1 = get_num_pbfs(output_path_1)

        config_path_2 = "/tiler-data/test-data/configs/merge2.tiler.json"
        self.assertTrue(os.path.isfile(config_path_2))
        tiles_from_config(config_path_2)
        output_path_2 = "/tiler-data/tiles/merge_2"
        self.assertTrue(os.path.isdir(output_path_1))
        num_pbfs_2 = get_num_pbfs(output_path_2)

        total = num_pbfs_1 + num_pbfs_2

        merge_tile_directories(output_path_1, output_path_2, overwrite=False)
        num_pbfs_total = get_num_pbfs(output_path_2)
        self.assertEqual(total, num_pbfs_total)


