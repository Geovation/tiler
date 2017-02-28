#!/bin/bash
# Shapefile, Database User, Database Name, Database Password, Table Name
echo $1
echo $2
ogr2ogr -f "ESRI Shapefile" "$1" PG:"host=localhost port=5432 user=$DB_USER dbname=$DB_NAME password=$DB_PASSWORD" "$2"