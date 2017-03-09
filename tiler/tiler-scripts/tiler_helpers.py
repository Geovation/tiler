import os
import json

def check_environ_vars():
    ## Check all environment variables are defined
    env_vars = ['DB_NAME', 'DB_USER', 'DB_PORT', 'DB_HOST', 'DB_PASSWORD']
    for env_var in env_vars:
        if env_var not in os.environ:
            raise ValueError("Necessary environment variable not set not: ", env_var) 


def check_file(FILE_NAME):
    if not os.path.isfile(FILE_NAME):
        raise OSError(FILE_NAME + " does not exist")


def add_tippecanoe_config(OUTPUT_PATH, LAYER_CONFIG):
    print "\n Rewriting GeoJSON to add tippecanoe options"
    with open(OUTPUT_PATH, 'r+') as geojson_file:
            geojson = json.load(geojson_file)
            for feature in geojson["features"]:
                feature["tippecanoe"] = {}
                if "layer" in LAYER_CONFIG:
                    feature["tippecanoe"]["layer"] = str(LAYER_CONFIG["layer"])
                if "maxzoom" in LAYER_CONFIG:
                    feature["tippecanoe"]["maxzoom"] = int(LAYER_CONFIG["maxzoom"])
                if "minzoom" in LAYER_CONFIG:
                    feature["tippecanoe"]["minzoom"] = int(LAYER_CONFIG["minzoom"])
            
            geojson_file.seek(0)
            geojson_file.write(json.dumps(geojson))
            geojson_file.truncate()


def absolute_file_paths(directory):
   for dirpath,_,filenames in os.walk(directory):
       for f in filenames:
           yield os.path.abspath(os.path.join(dirpath, f))