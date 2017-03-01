#!/usr/bin/python2.7
import psycopg2
import sys
import os
import subprocess

## Check all our variables are in order
if len(sys.argv) > 1:
    FILE_NAME = sys.argv[1]
else:
    raise  ValueError("FILE_NAME not defined")

if len(sys.argv) > 2:
    TABLE_NAME = sys.argv[2]
else:
    raise  ValueError("TABLE_NAME not defined" )

## Check all environment variables are defined
env_vars = ['DB_NAME', 'DB_USER', 'DB_PORT', 'DB_HOST', 'DB_PASSWORD']
for env_var in env_vars:
    if env_var not in os.environ:
        print env_var, "environment variable not set not"

if not os.path.isfile(FILE_NAME):
    raise IOError(FILE_NAME + " does not exist")

try:
    connect_command = 'ogr2ogr -f "PostgreSQL" PG:"host={} port={} user={} dbname={} password={}" -nlt PROMOTE_TO_MULTI {} -nln {} -append --config OGR_TRUNCATE YES'.format(
        os.environ['DB_HOST'],
        os.environ['DB_PORT'],
        os.environ['DB_USER'],
        os.environ['DB_NAME'], 
        os.environ['DB_PASSWORD'],
        FILE_NAME, 
        TABLE_NAME
    )
    print "\n Executing: ", connect_command
    process = subprocess.Popen(connect_command, shell=True)
    
    stdout, stderr = process.communicate()
    print stdout, stderr
    "Exit code: ", process.wait()
    
    print "\n Data from ", FILE_NAME, " added to ", TABLE_NAME, " sucessfully"

except Exception as err:
    print "Failed to add data from ", FILE_NAME, " to ", TABLE_NAME, ": ", err
    raise