#!/usr/bin/python2.7
import sys
import json
import os
from shapefile2geojson import shapefile2geojson
from geojson2tiles import *
from validate_geojson import validate_geojson
from tiler_helpers import add_tippecanoe_config
from postgis2geojson import postgis2geojson
from remote_file import *

def get_config(config_path):
    """ Open a Tiler config and return it as a dictonary """

    with open(config_path) as config_json:
            config_dict = json.load(config_json)
            return config_dict


def tiles_from_config(config_file):
    """ Create a set of tiles based off the settings in a config file """

    geojson_file_paths = []
    if type(config_file) == str:
        config_dict = get_config(config_file)
    elif type(config_file) == dict:
        config_dict = config_file
    else:
        raise TypeError("Must be path to config file or loaded config file as dict")

    # TODO: This should probably be in config validation!

    if "outdir" not in config_dict:
        raise "No outdir property in json. The outbound \
               directory should be of format 'outdir : path/to/dir'"
    else:
        OUTDIR = config_dict["outdir"]

    if "data" not in config_dict:
        raise "No data property in json. "
    else:
        DATA = config_dict["data"]

    if "update" not in config_dict:
        UPDATE = False
    else:
        UPDATE = config_dict["update"]

    if "tileset" not in config_dict:
        raise "No tileset property in json. "
    else:
        TILESET_NAME = config_dict["tileset"]

    if "simplification" not in config_dict:
        raise "No simplification property in json. "
    else:
        SIMPLIFICATION = config_dict["simplification"]

    MIN_ZOOM = None
    MAX_ZOOM = None

    for layer_name in DATA:
        layer_config = DATA[layer_name]
        print "\n Layer config : ", layer_config

        # SHAPEFILE
        if layer_config["type"] == "shapefile":
            for path in layer_config["paths"]:
                if is_url(path):
                    # raise OSError(path)
                    output_dir = "/tiler-data/input/"
                    downloaded_path = download(path, output_dir)
                    if is_zipfile(downloaded_path):
                        base = os.path.basename(downloaded_path)
                        base = os.path.splitext(base)[0]
                        end_dir = output_dir + "/" + base
                        unzip(downloaded_path, end_dir)

                        shapefile = end_dir + "/" + base + ".shp"
                        path = shapefile


                geojson_path = handle_shapefile(path, layer_name, layer_config)
                geojson_file_paths.append(geojson_path)

        # GEOJSON
        if layer_config["type"] == "geojson":
            for path in layer_config["paths"]:
                if is_url(path):
                    output_dir = "/tiler-data/input/"
                    path = download(path, output_dir)
                geojson_path = handle_geojson(path, layer_name, layer_config)
                geojson_file_paths.append(geojson_path)

        # POSTGIS
        if layer_config["type"] == "postgis":
            if "query" not in layer_config:
                raise TypeError("Query string not set in configuration file: ", config_file)
            query = layer_config["query"] # Table name translates to the layer name!
            geojson_path = handle_postgis(query, layer_name, layer_config)
            geojson_file_paths.append(geojson_path)

        if "minzoom" in layer_config:
            if MIN_ZOOM is None or layer_config["minzoom"] < MIN_ZOOM:
                MIN_ZOOM = layer_config["minzoom"]

        if "maxzoom" in layer_config:
            if MAX_ZOOM is None or layer_config["maxzoom"] > MAX_ZOOM:
                MAX_ZOOM = layer_config["maxzoom"]

    geojson2tiles(
        geojson_file_paths,
        TILESET_NAME,
        MIN_ZOOM=MIN_ZOOM,
        MAX_ZOOM=MAX_ZOOM,
        SIMPLIFICATION=SIMPLIFICATION,
        UPDATE=UPDATE
    )


def handle_remote_download(url):
    """ Handle the downloading of a remote file """

    output_dir = "/tiler-data/output/"
    download(url, output_dir)


def handle_postgis(query, layer_name, layer_config):
    """ Handle getting data from a PostGIS database """

    db_vars = os.environ
    # Layer Config we do it ourself manaully
    postgis2geojson(layer_name, db_vars, LAYER_CONFIG=layer_config, QUERY=query)
    geojson_path = "/tiler-data/geojson/{}.geojson".format(layer_name)
    add_config(geojson_path, layer_name, layer_config)
    return geojson_path


def handle_geojson(geojson_path, layer_name, layer_config):
    """ Handle getting data from a GeoJSON file """

    add_config(geojson_path, layer_config, layer_name)
    return geojson_path


def handle_shapefile(shp_path, layer_name, layer_config):
    """ Handle getting data from a shapefile """

    minzoom = layer_config["minzoom"]
    maxzoom = layer_config["maxzoom"]
    geojson_layer_config = {"minzoom" : minzoom, "maxzoom" : maxzoom, "layer": layer_name}
    shapefile2geojson(shp_path, layer_name, LAYER_CONFIG=geojson_layer_config)
    return "/tiler-data/geojson/{}.geojson".format(layer_name)


def add_config(path, layer_name, layer_config):
    """ Setup the tippecanoe config for use with tippecanoe """

    if "minzoom" in layer_config or "maxzoom" in layer_config or layer_name:
        tippecanoe_config = {}
        if "minzoom" in layer_config:
            tippecanoe_config["minzoom"] = layer_config["minzoom"]
        if "maxzoom" in layer_config:
            tippecanoe_config["maxzoom"] = layer_config["maxzoom"]
        if layer_name:
            tippecanoe_config["layer"] = layer_name
        add_tippecanoe_config(path, tippecanoe_config)


if __name__ == '__main__':

    print "\n Checking input variables are valid..."

    if len(sys.argv) > 1:
        CONFIG = sys.argv[1]
    else:
        raise ValueError("Config file has not been defined")

    CONFIG_FILE = "/tiler-data/configs/" + CONFIG + ".tiler.json"
    tiles_from_config(CONFIG_FILE)
    