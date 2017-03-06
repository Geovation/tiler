#!/usr/bin/python2.7
import psycopg2
import sys
import os
import subprocess
import tiler_helpers

def postgis2geojson(TABLE_NAME, DATABASE_VARS, LAYER_CONFIG=False)

    OUTPUT_PATH = "/tiler-data/geojson/{}.geojson".format(TABLE_NAME)
    try:
        os.remove(OUTPUT_PATH)
    except OSError:
        pass

    try:
        connect_command = """ogr2ogr -f GeoJSON {} PG:"host={} port={} user={} dbname={} password={}" -sql "select * from {}" """.format(
            OUTPUT_PATH,
            DATABASE_VARS['DB_HOST'],
            DATABASE_VARS['DB_PORT'],
            DATABASE_VARS['DB_USER'],
            DATABASE_VARS['DB_NAME'], 
            DATABASE_VARS['DB_PASSWORD'],
            TABLE_NAME
        )
        print "\n Executing: ", connect_command
        process = subprocess.Popen(connect_command, shell=True)
        
        stdout, stderr = process.communicate()
        print stdout, stderr
        "Exit code: ", process.wait()
        
        print "\n Database table", TABLE_NAME, "converted to", TABLE_NAME + ".geojson \n"

    if LAYER_CONFIG:
        add_tippecanoe_config(OUTPUT_PATH, LAYER_CONFIG)

    except Exception as err:
        print "Failed to convert to GeoJSON for table ", TABLE_NAME
        raise



if __name__ == '__main__':

    if len(sys.argv) > 1:
        TABLE_NAME = sys.argv[1]
    else:
        raise  ValueError("TABLE_NAME not defined" )

    tiler_helpers.check_environ_vars()
    DATABASE_VARS = os.environ
    postgis2geojson(TABLE_NAME, DATABASE_VARS)

