#!/bin/bash
# Output GeoJSON, Database User, Database Name, Database Password, Table Name
ogr2ogr -f GeoJSON ../tiles/$1.geojson \
  PG:"host=localhost port=5432 user=$DB_USER dbname=$DB_NAME password=$DB_PASSWORD" \ 
  -sql "select * from $2"