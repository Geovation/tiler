#!/usr/bin/python2.7
import sys
import os
import subprocess
import gzip
import shutil
from validate_geojson import validate_geojson
from tiler_helpers import absolute_file_paths

def create_vector_tiles(GEOJSON_FILES, MBTILES_NAME, MIN_ZOOM, MAX_ZOOM, SIMPLIFICATION, SPLIT=True, VALIDATE=False):
    """Create an .mbtiles file for a set of GeoJSON files"""

    if type(GEOJSON_FILES) != list:
        raise TypeError("GEOJSON_FILES is not a list")

     # Validate GeoJSON
    if VALIDATE == True:
        print "\n Validating GeoJSON"
        for geojson in GEOJSON_FILES:
            validate_geojson(geojson)
        print "\n GeoJSON is valid!"

    OUTPUT_PATH = "/tiler-data/tiles/{}".format(MBTILES_NAME)

    # Remove the current mbtiles file if it's there
    try:
        print "Tiles directory of that name already exists, removing it so it can be recreated"
        shutil.rmtree(OUTPUT_PATH)
    except OSError:
        pass

    if not os.path.exists("/tiler-data/tiles/"):
        os.makedirs("/tiler-data/tiles/")

    print "Commencing running creation of mbiles from GeoJSON files : ", str(GEOJSON_FILES)

    GEOJSON_FILES_STR = ""
    for geojson_file in GEOJSON_FILES:
        GEOJSON_FILES_STR += geojson_file + " "

    if SPLIT == False and MIN_ZOOM != None and MAX_ZOOM != None:
        command = "tippecanoe --output-to-directory {} {} --no-tile-compression --read-parallel --minimum-zoom={} --maximum-zoom={} --simplification={} --drop-smallest-as-needed --coalesce".format(OUTPUT_PATH, GEOJSON_FILES_STR, MIN_ZOOM, MAX_ZOOM, SIMPLIFICATION)

    elif MIN_ZOOM != None and MAX_ZOOM != None:
        print "\n Min Zoom: ", MIN_ZOOM
        print "\n Max Zoom: ", MAX_ZOOM
        command = "tippecanoe --output-to-directory {} {} --no-tile-compression  --read-parallel --minimum-zoom={}  --maximum-zoom={} --no-polygon-splitting --simplification={} --drop-smallest-as-needed --coalesce".format(OUTPUT_PATH, GEOJSON_FILES_STR, MIN_ZOOM, MAX_ZOOM, SIMPLIFICATION)
    else:
        command = "tippecanoe --output-to-directory {} {} --no-tile-compression --read-parallel --no-polygon-splitting --simplification={} --drop-smallest-as-needed --coalesce".format(OUTPUT_PATH, GEOJSON_FILES_STR, SIMPLIFICATION)

    print "\n Running: ", command
    FNULL = open(os.devnull, 'w')
    tippecanoe_exit_code = subprocess.call(command, shell=True)# stdout=FNULL, stderr=subprocess.STDOUT)
    print "\n Tippecanoe exit code: ", tippecanoe_exit_code
    if tippecanoe_exit_code != 0:
        raise IOError("Exit code was not 0 for tippecanoe process")

    print "\n Created tiles from " + str(GEOJSON_FILES)


def create_demo_config(MBTILES_NAME):
    """ Generate a config for the web demos """

    demo_config = "/tiler-data/configs/web-demo-config.js"
    with open(demo_config, 'w+') as f:
        config = "var vectortiles = '" + MBTILES_NAME + "';"
        f.seek(0)
        f.write(config)
        f.truncate()

def geojson2tiles(GEOJSON_FILES, MBTILES_NAME, MIN_ZOOM, MAX_ZOOM, SIMPLIFICATION=0, UPDATE=False, VALIDATE=False):
    """ From a set of GeoJSON files generate a set of raw protobuf vector tiles """

    print "\n Running geojson2tiles..."

    assert isinstance(SIMPLIFICATION, int)

    if MIN_ZOOM != None and MAX_ZOOM != None:
        assert isinstance(MIN_ZOOM, int)
        assert isinstance(MAX_ZOOM, int)
        assert MAX_ZOOM > MIN_ZOOM

    create_vector_tiles(GEOJSON_FILES, MBTILES_NAME, MIN_ZOOM, MAX_ZOOM, SIMPLIFICATION, UPDATE, VALIDATE)
    create_demo_config(MBTILES_NAME)


if __name__ == '__main__':

    print "\n Checking input variables are valid..."

    if len(sys.argv) > 1:
        GEOJSON_FILE = sys.argv[1]
    else:
        raise ValueError("GEOJSON_FILE not defined")

    if len(sys.argv) > 2:
        MIN_ZOOM = int(sys.argv[2])
    else:
        MIN_ZOOM = "0" #raise ValueError("MAX_ZOOM not defined")

    if len(sys.argv) > 3:
        MAX_ZOOM = int(sys.argv[3])
    else:
        raise ValueError("MAX_ZOOM not defined")

    if len(sys.argv) > 4:
        SIMPLIFICATION = int(sys.argv[4])
    else:
        SIMPLIFICATION = "0"

    if not os.path.isfile(GEOJSON_FILE):
        raise IOError(GEOJSON_FILE + " does not exist")

    print "\n Input variables are valid!"

    MBTILES_NAME = os.path.basename(os.path.splitext(GEOJSON_FILE)[0])
    geojson2tiles([GEOJSON_FILE], MBTILES_NAME, MIN_ZOOM, MAX_ZOOM, SIMPLIFICATION)
