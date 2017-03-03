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

def create_mbtiles(GEOJSON_FILE, MBTILES_NAME, MAX_ZOOM, MIN_ZOOM, SIMPLIFICATION):

    # Validate GeoJSON 
    print "\n Validating GeoJSON"
    validate_geojson(GEOJSON_FILE)
    print "\n GeoJSON is valid!"

    # Create .mbtiles file
    OUTPUT_PATH = "/tiler-data/tiles/{}.mbtiles".format(MBTILES_NAME)

    # Remove the current mbtiles file if it's there
    try:
        print "MBTiles file of that name already exists, removing it so it can be recreated"
        os.remove(OUTPUT_PATH)
    except OSError:
        pass

    print "Commencing running creation of mbiles from GeoJSON file", GEOJSON_FILE
    command = "tippecanoe -o {} {} --maximum-zoom={} --minimum-zoom={} --read-parallel --no-polygon-splitting --simplification={} --drop-smallest-as-needed --coalesce".format(OUTPUT_PATH, GEOJSON_FILE, MAX_ZOOM, MIN_ZOOM, SIMPLIFICATION)
    print "\n Running: ", command
    tippecanoe_process = subprocess.Popen(command, shell=True)
    stdout, stderr = tippecanoe_process.communicate()
    # print stdout, stderr
    print "\n Exit code: ", tippecanoe_process.wait()

    print "\n Created mbtiles file from " + GEOJSON_FILE


def extract_pbf(MBTILES_NAME):
    
    MBTILES_DIR = os.path.join("tiles", MBTILES_NAME)
    # Create unzipped .pbf 
    if os.path.isdir(MBTILES_DIR):
        print "\n Vector Tiles folder (", MBTILES_DIR, ") already exists removing it..."
        try:
            shutil.rmtree(MBTILES_DIR)
        except OSError as shutil_err:
            print shutil_err
            print "\n shutil.rmtree failed for one reason or another, trying rm -rf ..."
            try:
                os.system("rm -rf " + MBTILES_DIR)
            except OSError as os_err:
                print "\n That failed too... unable to remove the directory"
                raise os_err

        print "\n Vector Tiles folder removed!"

    print "\n Commencing extraction from mbtiles to", MBTILES_DIR
    command = "mb-util --image_format=pbf /tiler-data/tiles/{}.mbtiles /tiler-data/tiles/{}".format(MBTILES_NAME, MBTILES_NAME, MBTILES_NAME)
    print "\n Running: ", command
    mbutil_process = subprocess.Popen(command, shell=True)
    stdout, stderr = mbutil_process.communicate()
    # print stdout, stderr
    print "\n Exit code: ", mbutil_process.wait()


def decompress_pbf(MBTILES_NAME):

    # We need to rename everything and then unzip it 
    print "\n Decompressing gzipped Vector Tiles"
    extension = ".pbf"
    length = len(extension)
    counter = 0
    for filename in absoluteFilePaths("tiles/" + MBTILES_NAME):

        if counter % 50 == 0:
            print "\n 10 more tiles decompressed..."
            
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

        counter += 1

    print "\n Vector Tiles decompressed!"

    print "\n Finished! See tiles/" + MBTILES_NAME, " for the resulting files \n"


if __name__ == '__main__':

    print "\n Checking input variables are valid..."

    if len(sys.argv) > 1:
        GEOJSON_FILE = sys.argv[1]
    else:
        raise ValueError("GEOJSON_FILE not defined" )

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

    create_mbtiles(GEOJSON_FILE, MBTILES_NAME, MAX_ZOOM, MIN_ZOOM, SIMPLIFICATION)
    extract_pbf(MBTILES_NAME)
    decompress_pbf(MBTILES_NAME)
