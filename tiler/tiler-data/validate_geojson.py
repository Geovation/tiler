import geojson
import sys

## Check all our variables are in order
if len(sys.argv) > 1:
    FILE_NAME = sys.argv[1]
else:
    raise  ValueError("FILE_NAME not defined")

## Validate the GeoJSON file
with open(FILE_NAME, 'r') as geojson_file:
    geojson_dump = geojson_file.read()
    features = geojson.loads(geojson_dump)
    validation = geojson.is_valid(features)

    print "Is the geojson file valid? ", validation["valid"]
    if validation["message"]:
        print "Info: ", validation["message"]



