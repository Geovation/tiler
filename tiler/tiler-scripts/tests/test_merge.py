import unittest
import sys, os
import shutil
import mapbox_vector_tile

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Insanity for getting parent folder in path
from tiler_helpers import absolute_file_paths
from tiler import tiles_from_config
from merge import merge_tile_directories, get_num_pbfs, copy_dir

class TestMerge(unittest.TestCase):

    def test_get_num_pbfs(self):
        self.assertEqual(get_num_pbfs("/tiler-data/test-data/test-tiles"), 594)

    def test_copy_dir(self):

        config_path_1 = "/tiler-data/test-data/configs/merge1.tiler.json"
        self.assertTrue(os.path.isfile(config_path_1))
        tiles_from_config(config_path_1)
        output_path_1 = "/tiler-data/tiles/test_merge_1"
        self.assertTrue(os.path.isdir(output_path_1))
        num_pbfs_1 = get_num_pbfs(output_path_1)

        output_path_1_copy = "/tiler-data/tiles/test_merge_1_copy"    
        copy_dir(output_path_1, output_path_1_copy)
        num_pbfs_1_copy = get_num_pbfs(output_path_1_copy)
        self.assertEqual(num_pbfs_1, num_pbfs_1_copy)
        
    def test_merge_tile_directories(self):

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
        
        out_dir = "/tiler-data/tiles/merge-test/"
        merge_tile_directories(output_path_1, output_path_2, out_dir)
        num_pbfs_total = get_num_pbfs("/tiler-data/tiles/merge-test/")
        self.assertEqual(total, num_pbfs_total)

    def test_merge_tile_directories_with_overlap(self):

        config_path_1 = "/tiler-data/test-data/configs/mergeOverlap1.tiler.json"
        self.assertTrue(os.path.isfile(config_path_1))
        tiles_from_config(config_path_1)
        output_path_1 = "/tiler-data/tiles/test_merge_overlap_1"
        self.assertTrue(os.path.isdir(output_path_1))

        config_path_2 = "/tiler-data/test-data/configs/mergeOverlap2.tiler.json"
        self.assertTrue(os.path.isfile(config_path_2))
        tiles_from_config(config_path_2)
        output_path_2 = "/tiler-data/tiles/test_merge_overlap_2"
        self.assertTrue(os.path.isdir(output_path_2))

        out_dir = "/tiler-data/tiles/merge-test-overlap/"
        merge_tile_directories(output_path_1, output_path_2, out_dir)

        with open("/tiler-data/tiles/merge-test-overlap/2/0/1.pbf", 'rb') as f:
            data = f.read()
        overlap_merge = mapbox_vector_tile.decode(data)        

        with open("/tiler-data/tiles/test_merge_overlap_1/2/0/1.pbf", 'rb') as f:
            data = f.read()
        overlap_1 = mapbox_vector_tile.decode(data)

        with open("/tiler-data/tiles/test_merge_overlap_2/2/0/1.pbf", 'rb') as f:
            data = f.read()
        overlap_2 = mapbox_vector_tile.decode(data)        

        self.assertTrue(os.path.isdir(out_dir))
        self.assertTrue(get_num_pbfs(out_dir) > 0)
        self.assertTrue(str(overlap_merge).find("Pizazz") and str(overlap_1).find("Pizazz"))
        self.assertEqual(str(overlap_2).find("Pizazz"), -1)
        self.assertTrue(str(overlap_merge).find("Hungry") and str(overlap_2).find("Hungry"))
        self.assertEqual(str(overlap_1).find("Hungry"), -1)

    def tearDown(self):
        try:
            print "\n Tearing down the tests..."
            os.remove("/tiler-data/geojson/test_stations.geojson")
            shutil.rmtree("/tiler-data/tiles/test_merge_1")
            shutil.rmtree("/tiler-data/tiles/test_merge_2")
            shutil.rmtree("/tiler-data/tiles/test_merge_1_copy")
            shutil.rmtree("/tiler-data/tiles/merge-test/")
        except OSError:
            pass

        try:
            print "\n Tearing down the overlap merge test..."
            shutil.rmtree("/tiler-data/tiles/test_merge_overlap_1")
            shutil.rmtree("/tiler-data/tiles/test_merge_overlap_2")
            shutil.rmtree("/tiler-data/tiles/merge-test-overlap")
        except OSError:
            pass

if __name__ == '__main__':
    unittest.main()