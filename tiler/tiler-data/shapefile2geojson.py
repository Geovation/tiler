#!/usr/bin/python2.7
import psycopg2
import sys
import os
import subprocess

if len(sys.argv) > 1:
    INPUT_PATH = sys.argv[1]
else:
    raise  ValueError("INPUT_PATH not defined" )

if len(sys.argv) > 1:
    OUTPUT_NAME = sys.argv[2]
else:
    raise  ValueError("OUTPUT_NAME not defined" )


OUTPUT = "/tiler-data/geojson/{}.geojson".format(OUTPUT_NAME)
try:
    os.remove(OUTPUT)
except OSError:
    pass

try:
    connect_command = """ogr2ogr -f GeoJSON {} {}""".format(OUTPUT, INPUT_PATH)
    print "\n Executing: ", connect_command
    process = subprocess.Popen(connect_command, shell=True)
    
    stdout, stderr = process.communicate()
    # print stdout, stderr
    "Exit code: ", process.wait()
    
    print "\n Shapefile", INPUT_PATH, "converted to", OUTPUT_NAME + ".geojson"

except Exception as err:
    print "Failed to convert to GeoJSON from Shapefile for ", INPUT_PATH
    raise