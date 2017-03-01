#!/usr/bin/python2.4
import sys
import os
import subprocess
import fnmatch
import glob
import gzip

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

if not os.path.isfile(GEOJSON_FILE):
    raise IOError(GEOJSON_FILE + " does not exist")


# ## Create .mbtiles file
MBTILES_NAME = os.path.basename(os.path.splitext(GEOJSON_FILE)[0])
print MBTILES_NAME
OUTPUT_PATH = "/tiler-data/tiles/{}.mbtiles".format(MBTILES_NAME)
try:
    os.remove(OUTPUT_PATH)
except OSError:
    pass

command = "tippecanoe -o {} {} --maximum-zoom={} --read-parallel".format(OUTPUT_PATH, GEOJSON_FILE, MAX_ZOOM)
print "Running: ", command
tippecanoe_process = subprocess.Popen(command, shell=True)
stdout, stderr = tippecanoe_process.communicate()
# print stdout, stderr
print "Exit code: ", tippecanoe_process.wait()

print "Created mbtiles file from " + GEOJSON_FILE

# ## Create unzipped .pbf 
command = "mb-util --image_format=pbf tiles/{}.mbtiles tiles/{}".format(MBTILES_NAME, MBTILES_NAME)
mbutil_process = subprocess.Popen(command, shell=True)
stdout, stderr = mbutil_process.communicate()
# print stdout, stderr
print "Exit code: ", mbutil_process.wait()

# We need to rename everything and then unzip it 
extension = ".pbf"
length = len(extension)
# gz_magic = "\x1f\x8b\x08" # Magic number used by gzip

for filename in absoluteFilePaths("tiles/" + MBTILES_NAME):

    if '.pbf' in filename:
        old_name = os.path.abspath(filename)
        new_name = old_name[:-length] + '.pbf.gz'

        if filename.endswith(".pbf"):
            os.rename(old_name, new_name)

        # Loop through and unzip everything to actually be a real .pbf file
        with gzip.open(new_name, 'rb') as infile:
            with open(old_name, 'wb') as outfile:
                for line in infile:
                    outfile.write(line)

        # Get rid of the renamed, unzipped file 
        os.remove(new_name)


