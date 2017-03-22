import os
import json

def check_environ_vars():
    """ Make sure database environment variables are present """

    ## Check all environment variables are defined
    env_vars = ['DB_NAME', 'DB_USER', 'DB_PORT', 'DB_HOST', 'DB_PASSWORD']
    for env_var in env_vars:
        if env_var not in os.environ:
            raise ValueError("Necessary environment variable not set not: ", env_var)


def check_file(file_name):
    """ Check a file exists """

    if not os.path.isfile(file_name):
        raise OSError(file_name + " does not exist")


def add_tippecanoe_config(output_path, layer_config):
    """ Given a configuration, add the configuration to a given GeoJSON file """

    print "\n Rewriting GeoJSON to add tippecanoe options"
    with open(output_path, 'r+') as geojson_file:
        geojson = json.load(geojson_file)
        for feature in geojson["features"]:
            feature["tippecanoe"] = {}
            if "layer" in layer_config:
                feature["tippecanoe"]["layer"] = str(layer_config["layer"])
            if "maxzoom" in layer_config:
                feature["tippecanoe"]["maxzoom"] = int(layer_config["maxzoom"])
            if "minzoom" in layer_config:
                feature["tippecanoe"]["minzoom"] = int(layer_config["minzoom"])

        geojson_file.seek(0)
        geojson_file.write(json.dumps(geojson))
        geojson_file.truncate()


def absolute_file_paths(directory):
    """ Get a generator of all the absolute paths for files in a directory """
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            yield os.path.abspath(os.path.join(dirpath, f))
