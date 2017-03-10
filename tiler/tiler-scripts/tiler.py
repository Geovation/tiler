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

def get_config(CONFIG_PATH):
    with open(CONFIG_PATH) as config_json:
            config_dict = json.load(config_json)
            return config_dict

def handle_config(CONFIG_FILE):

    geojson_file_paths = []
    config_dict = get_config(CONFIG_FILE)

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
                    output_dir = "/tiler-data/input/"
                    downloaded_path = download(path, output_dir)
                    if is_zip(downloaded_path):
                        downloaded_path = unzip(downloaded_path)
                        base = os.path.basename(downloaded_path)
                        shapefile = downloaded_path + "/" + base + ".shp"
                        path = shapefile
                
                geojson_path = handle_shapefile(path, layer_name, layer_config)
                geojson_file_paths.append(geojson_path)

        # GEOJSON
        if layer_config["type"] == "geojson":
            for path in layer_config["paths"]:
                geojson_path = handle_geojson(path, layer_name, layer_config)
                geojson_file_paths.append(geojson_path)

        # POSTGIS
        if layer_config["type"] == "postgis":
            if "query" not in layer_config:
                raise TypeError("Query string not set in configuration file: ", CONFIG_FILE)
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
        SIMPLIFICATION=SIMPLIFICATION
    )


def handle_remote_download(url):
    output_dir = "/tiler-data/output/"
    download(url, output_dir)


def handle_postgis(query, layer_name, layer_config):
    db_vars = os.environ
    postgis2geojson(None, db_vars, LAYER_CONFIG=layer_config, QUERY=query) # Layer Config we do it ourself manaully
    geojson_path = "/tiler-data/geojson/{}.geojson".format(layer_name)
    add_config(geojson_path, layer_name,  layer_config)
    return geojson_path


def handle_geojson(geojson_path, layer_name, layer_config):
    add_config(geojson_path, layer_config, layer_name)
    return geojson_path 


def handle_shapefile(shp_path, layer_name, layer_config):
    minzoom = layer_config["minzoom"]
    maxzoom = layer_config["maxzoom"]
    LAYER_CONFIG = {"minzoom" : minzoom, "maxzoom" : maxzoom, "layer": layer_name}
    shapefile2geojson(shp_path, layer_name, LAYER_CONFIG=LAYER_CONFIG)
    return "/tiler-data/geojson/{}.geojson".format(layer_name)


def add_config(path, layer_name, layer_config):
    if "minzoom" in layer_config or "maxzoom" in layer_config or layer_name:
        TIPPECANOE_CONFIG = {}
        if "minzoom" in layer_config:
            TIPPECANOE_CONFIG["minzoom"] = layer_config["minzoom"]
        if "maxzoom" in layer_config:
            TIPPECANOE_CONFIG["maxzoom"] = layer_config["maxzoom"]
        if layer_name:
            TIPPECANOE_CONFIG["layer"] = layer_name
        add_tippecanoe_config(path, TIPPECANOE_CONFIG)


if __name__ == '__main__':

    print "\n Checking input variables are valid..."

    if len(sys.argv) > 1:
        CONFIG = sys.argv[1]
    else:
        raise ValueError("Config file has not been defined")

    CONFIG_FILE = "/tiler-data/configs/" + CONFIG + ".tiler.json"
    handle_config(CONFIG_FILE)
    