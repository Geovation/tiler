#!/usr/bin/python2.4
import sys
import os
import subprocess
import fnmatch
import glob
import gzip
import shutil
from validate_geojson import validate_geojson

def absoluteFilePaths(directory):
   for dirpath,_,filenames in os.walk(directory):
       for f in filenames:
           yield os.path.abspath(os.path.join(dirpath, f))

if len(sys.argv) > 1:
    GEOJSON_FILE = sys.argv[1]
else:
    raise ValueError("GEOJSON_FILE not defined" )

if len(sys.argv) > 2:
    MAX_ZOOM = int(sys.argv[2])
else:
    raise ValueError("MAX_ZOOM not defined" )

if len(sys.argv) > 3:
    SIMPLIFICATION = int(sys.argv[3])
else:
    SIMPLIFICATION = "0"

if not os.path.isfile(GEOJSON_FILE):
    raise IOError(GEOJSON_FILE + " does not exist")



SIMPLIFICATION


# Validate GeoJSON 
validate_geojson(GEOJSON_FILE)


# Create .mbtiles file
MBTILES_NAME = os.path.basename(os.path.splitext(GEOJSON_FILE)[0])
MBTILES_DIR = os.path.join("tiles", MBTILES_NAME)
OUTPUT_PATH = "/tiler-data/tiles/{}.mbtiles".format(MBTILES_NAME)

# Remove the current mbtiles file if it's there
try:
    os.remove(OUTPUT_PATH)
except OSError:
    pass

command = "tippecanoe -o {} {} --maximum-zoom={} --read-parallel --no-polygon-splitting --simplification={} ".format(OUTPUT_PATH, GEOJSON_FILE, MAX_ZOOM, SIMPLIFICATION)
print "\n Running: ", command
tippecanoe_process = subprocess.Popen(command, shell=True)
stdout, stderr = tippecanoe_process.communicate()
# print stdout, stderr
print "\n Exit code: ", tippecanoe_process.wait()

print "\n Created mbtiles file from " + GEOJSON_FILE

# Create unzipped .pbf 
if os.path.isdir(MBTILES_DIR):
    print "\n Vector Tiles folder (", MBTILES_DIR, ") already exists removing it..."
    shutil.rmtree(MBTILES_DIR)
    print "\n Vector Tiles folder removed!"

command = "mb-util --image_format=pbf /tiler-data/tiles/{}.mbtiles /tiler-data/tiles/{}".format(MBTILES_NAME, MBTILES_NAME, MBTILES_NAME)
print "\n Running: ", command
mbutil_process = subprocess.Popen(command, shell=True)
stdout, stderr = mbutil_process.communicate()
# print stdout, stderr
print "\n Exit code: ", mbutil_process.wait()

# We need to rename everything and then unzip it 
extension = ".pbf"
length = len(extension)
# gz_magic = "\x1f\x8b\x08" # Magic number used by gzip


for filename in absoluteFilePaths("tiles/" + MBTILES_NAME):

    if filename.endswith(".pbf"):
        old_name = os.path.abspath(filename)
        new_name = old_name[:-length] + '.pbf.gz'
        os.rename(old_name, new_name)

        # Loop through and unzip everything to actually be a real .pbf file
        with gzip.open(new_name, 'rb') as infile:
            with open(old_name, 'wb') as outfile:
                for line in infile:
                    outfile.write(line)

        # Get rid of the renamed, unzipped file 
        os.remove(new_name)


