#!/usr/bin/python2.7
import sys
import os
import subprocess
import fnmatch
import glob
import gzip
import shutil
import json
from shapefile2geojson import *
from geojson2tiles import *
from validate_geojson import validate_geojson


def handle_config(CONFIG_FILE):

    geojson_file_paths = []

    with open(CONFIG_FILE) as config_json:
        config_dict = json.load(config_json)
        if "outdir" not in config_dict:
            raise "No outdir property in json. The outbound directory should be of format 'outdir : path/to/dir'"
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

        for layer_name in DATA:
            layer_config = DATA[layer_name]
            print "\n Layer config : ", layer_config
            if layer_config["type"] == "shapefile":
                for path in layer_config["paths"]:
                    geojson_path = handle_shapefile(path, layer_name, layer_config)
                    geojson_file_paths.append(geojson_path)
        
        geojson2tiles(geojson_file_paths, TILESET_NAME, MIN_ZOOM=None, MAX_ZOOM=None, SIMPLIFICATION=SIMPLIFICATION)


def handle_shapefile(path, layer_name, layer_config):

    minzoom = layer_config["minzoom"]
    maxzoom = layer_config["maxzoom"]
    LAYER_CONFIG = {"minzoom" : minzoom, "maxzoom" : maxzoom, "layer": layer_name}
    shapefile2geojson(path, layer_name, LAYER_CONFIG=LAYER_CONFIG)
    return "/tiler-data/geojson/{}.geojson".format(layer_name)

if __name__ == '__main__':

    print "\n Checking input variables are valid..."

    if len(sys.argv) > 1:
        CONFIG = sys.argv[1]
    else:
        raise ValueError("Config file has not been defined" )

    CONFIG_FILE = "/tiler-data/configs/" + CONFIG + ".tiler.json"
    handle_config(CONFIG_FILE)


