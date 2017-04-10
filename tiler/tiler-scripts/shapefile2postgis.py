#!/usr/bin/python2.7
import psycopg2
import sys
import os
import subprocess
import tiler_helpers


def shapefile2postgis(FILE_NAME, TABLE_NAME, DB_VARS):
    """ Convert a shapefile to a PostGIS table """

    tiler_helpers.check_file(FILE_NAME)

    try:
        connect_command = 'ogr2ogr -f "PostgreSQL" PG:"host={} port={} user={} dbname={} password={}" -nlt PROMOTE_TO_MULTI {} -nln {} -append --config OGR_TRUNCATE YES'.format(
            DB_VARS['DB_HOST'],
            DB_VARS['DB_PORT'],
            DB_VARS['DB_USER'],
            DB_VARS['DB_NAME'],
            DB_VARS['DB_PASSWORD'],
            FILE_NAME,
            TABLE_NAME
        )
        print "\n Executing: ", connect_command
        process = subprocess.Popen(connect_command, shell=True)

        stdout, stderr = process.communicate()
        print stdout, stderr
        print "Exit code: ", process.wait()

        print "\n Data from ", FILE_NAME, " added to ", TABLE_NAME, " sucessfully"

    except Exception as err:
        print "Failed to add data from ", FILE_NAME, " to ", TABLE_NAME, ": ", err
        raise



if __name__ == '__main__':

    ## Check all our variables are in order
    if len(sys.argv) > 1:
        FILE_NAME = sys.argv[1]
    else:
        raise  ValueError("FILE_NAME not defined")

    if len(sys.argv) > 2:
        TABLE_NAME = sys.argv[2]
    else:
        raise  ValueError("TABLE_NAME not defined")

    ## Check all PostgreSQL environment variables are defined
    tiler_helpers.check_environ_vars()
    shapefile2postgis(FILE_NAME, TABLE_NAME, os.environ)
  