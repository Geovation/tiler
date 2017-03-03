#!/usr/bin/python2.7
import psycopg2
import sys
import os
import subprocess

if len(sys.argv) > 1:
    TABLE_NAME = sys.argv[1]
else:
    raise  ValueError("TABLE_NAME not defined" )

## Check all environment variables are defined
env_vars = ['DB_NAME', 'DB_USER', 'DB_PORT', 'DB_HOST', 'DB_PASSWORD']
for env_var in env_vars:
    if env_var not in os.environ:
        print env_var, "environment variable not set not"


OUTPUT = "/tiler-data/geojson/{}.geojson".format(TABLE_NAME)
try:
    os.remove(OUTPUT)
except OSError:
    pass

try:
    connect_command = """ogr2ogr -f GeoJSON {} PG:"host={} port={} user={} dbname={} password={}" -sql "select * from {}" """.format(
        OUTPUT,
        os.environ['DB_HOST'],
        os.environ['DB_PORT'],
        os.environ['DB_USER'],
        os.environ['DB_NAME'], 
        os.environ['DB_PASSWORD'],
        TABLE_NAME
    )
    print "\n Executing: ", connect_command
    process = subprocess.Popen(connect_command, shell=True)
    
    stdout, stderr = process.communicate()
    print stdout, stderr
    "Exit code: ", process.wait()
    
    print "\n Database table", TABLE_NAME, "converted to", TABLE_NAME + ".geojson \n"

except Exception as err:
    print "Failed to convert to GeoJSON for table ", TABLE_NAME
    raise