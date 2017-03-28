#!/usr/bin/python2.7
import psycopg2
import sys
import os
import subprocess
from tiler_helpers import add_tippecanoe_config, check_environ_vars

def postgis2geojson(TABLE_NAME, DATABASE_VARS, LAYER_CONFIG=False, QUERY=False):
    """ Take data from tables in PostGIS and export them to GeoJSON """

    if not TABLE_NAME and not QUERY:
        raise ValueError("No parameters passed for a valid SQL query")

    if QUERY:
        query = QUERY
    else:
        query = "select * from {}".format(TABLE_NAME)

    OUTPUT_PATH = "/tiler-data/geojson/{}.geojson".format(TABLE_NAME)
    try:
        os.remove(OUTPUT_PATH)
    except OSError:
        pass

    connect_command = """ogr2ogr -f GeoJSON {} -t_srs EPSG:4326 PG:"host={} port={} user={} dbname={} password={}" -sql "{}" """.format(
        OUTPUT_PATH,
        DATABASE_VARS['DB_HOST'],
        DATABASE_VARS['DB_PORT'],
        DATABASE_VARS['DB_USER'],
        DATABASE_VARS['DB_NAME'],
        DATABASE_VARS['DB_PASSWORD'],
        query
    )
    print "\n Executing: ", connect_command
    process = subprocess.Popen(connect_command, shell=True)

    stdout, stderr = process.communicate()
    print stdout, stderr
    exit_code = process.wait()
    print "\n Exit code: ", exit_code
    if exit_code != 0:
        raise OSError("Failed to execute the SQL query correctly: " + query)

    print "\n GeoJSON created"

    if LAYER_CONFIG != False:
        add_tippecanoe_config(OUTPUT_PATH, LAYER_CONFIG)


if __name__ == '__main__':

    if len(sys.argv) > 1:
        TABLE_NAME = sys.argv[1]
    else:
        raise  ValueError("TABLE_NAME not defined")

    check_environ_vars()
    DATABASE_VARS = os.environ
    postgis2geojson(TABLE_NAME, DATABASE_VARS)

