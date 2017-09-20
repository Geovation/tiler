import geojson
import sys

def validate_geojson(geojson_path):
    """ Validate a GeoJSON file """

    ## Validate the GeoJSON file
    with open(geojson_path, 'r') as geojson_file:
        geojson_dump = geojson_file.read()
        features = geojson.loads(geojson_dump)
        validation = features.is_valid
        
        print "Is the geojson file valid? ", str(validation)
        # if validation["message"]:
        #     print "Info: ", validation["message"]

        return validation

if __name__ == '__main__':

    ## Check all our variables are in order
    if len(sys.argv) > 1:
        FILE_NAME = sys.argv[1]
    else:
        raise  ValueError("FILE_NAME not defined")

    validate_geojson(FILE_NAME)
