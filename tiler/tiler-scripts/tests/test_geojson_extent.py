import unittest
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Insanity for getting parent folder in path
from geojson_extent import geojson_extent
 
class TestGeoJsonExtent(unittest.TestCase):
    """Tests geojson extent return correct extent for geojson file"""
 
    def test_extent(self):
        """Does geojson_extent return the correct bounding box of cupcakes.geojson?"""
        GEOJSON_FILE = "/tiler-data/test-data/cupcakes.geojson"        
        CUPCAKES_BBOX = [-122.92043, 45.376817, -122.477791, 45.649718]
        self.assertEqual(geojson_extent(GEOJSON_FILE), CUPCAKES_BBOX)

if __name__ == '__main__':
    unittest.main()