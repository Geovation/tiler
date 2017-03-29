#!/usr/bin/python2.7
import psycopg2
import sys
import os
import subprocess
import json
import tiler_helpers


def shapefile2geojson(INPUT_PATH, OUTPUT_NAME, LAYER_CONFIG=False):
    """ Convert a shapefile to a GeoJSON file """

    tiler_helpers.check_file(INPUT_PATH)

    if not os.path.exists("/tiler-data/geojson"):
        os.makedirs("/tiler-data/geojson")

    OUTPUT_PATH = "/tiler-data/geojson/{}.geojson".format(OUTPUT_NAME)
    try:
        os.remove(OUTPUT_PATH)
    except OSError:
        pass

    try:
        connect_command = """ogr2ogr -f GeoJSON -t_srs EPSG:4326 {} {}""".format(OUTPUT_PATH,
                                                                                 INPUT_PATH)
        print "\n Executing: ", connect_command
        process = subprocess.Popen(connect_command, shell=True)

        stdout, stderr = process.communicate()
        # print stdout, stderr
        "\n Exit code: ", process.wait()

        print "\n Shapefile", INPUT_PATH, "converted to", OUTPUT_NAME + ".geojson \n"

        if LAYER_CONFIG:
            tiler_helpers.add_tippecanoe_config(OUTPUT_PATH, LAYER_CONFIG)

    except Exception as err:
        print "Failed to convert to GeoJSON from Shapefile for ", INPUT_PATH
        raise


if __name__ == '__main__':

    if len(sys.argv) > 1:
        INPUT_PATH = sys.argv[1]
    else:
        raise  ValueError("INPUT_PATH not defined" )

    if len(sys.argv) > 1:
        OUTPUT_NAME = sys.argv[2]
    else:
        raise  ValueError("OUTPUT_NAME not defined" )
    
    shapefile2geojson(INPUT_PATH, OUTPUT_NAME)

