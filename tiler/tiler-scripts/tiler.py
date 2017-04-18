#!/usr/bin/python2.7
import sys
import json
import os
from shapefile2geojson import shapefile2geojson
from geojson2tiles import *
from validate_geojson import validate_geojson
from tiler_helpers import add_tippecanoe_config
from postgis2geojson import postgis2geojson
from shapefile2postgis import shapefile2postgis
from gml2geojson import gml2geojson
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

    # Insure GeoJSON path exists
    if not os.path.exists("/tiler-data/geojson"):
       os.makedirs("/tiler-data/geojson")

    OUTDIR = config_dict["outdir"]
    DATA = config_dict["data"]

    if "validate" not in config_dict:
        VALIDATE = False
    else:
        VALIDATE = config_dict["validate"]

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

            database_insert = False

            if "databaseInsert" in layer_config and layer_config["databaseInsert"] == True:
                database_insert = True

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
                    else:
                        raise TypeError("Downloaded shapefile is not a zipfile. Shapefile have 3 mandatory files so must be zipped!")

                geojson_path = handle_shapefile(path, layer_name, layer_config, database_insert)
                geojson_file_paths.append(geojson_path)

        # GEOJSON
        if layer_config["type"] == "geojson":
            for path in layer_config["paths"]:
                if is_url(path):
                    output_dir = "/tiler-data/input/"
                    path = download(path, output_dir)
                geojson_path = handle_geojson(path, layer_name, layer_config)
                geojson_file_paths.append(geojson_path)


        # GML
        if layer_config["type"] == "gml":

            database_insert = False

            if "databaseInsert" in layer_config and layer_config["databaseInsert"] == True:
                database_insert = True

            for path in layer_config["paths"]:
                if is_url(path):
                    output_dir = "/tiler-data/input/"
                    path = download(path, output_dir)

                geojson_path = handle_gml(path, layer_name, layer_config, database_insert)
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
        UPDATE=UPDATE,
        VALIDATE=VALIDATE
    )


def handle_remote_download(url):
    """ Handle the downloading of a remote file """

    output_dir = "/tiler-data/output/"
    download(url, output_dir)

def get_clean_config(layer_config, layer_name):
    minzoom = layer_config["minzoom"]
    maxzoom = layer_config["maxzoom"]
    return {"minzoom" : minzoom, "maxzoom" : maxzoom, "layer": layer_name}


def handle_postgis(query, layer_name, layer_config):
    """ Handle getting data from a PostGIS database """

    db_vars = os.environ
    geojson_layer_config = get_clean_config(layer_config, layer_name)

    postgis2geojson(layer_name, db_vars, LAYER_CONFIG=geojson_layer_config, QUERY=query)
    geojson_path = "/tiler-data/geojson/{}.geojson".format(layer_name)
    return geojson_path


def handle_geojson(geojson_path, layer_name, layer_config):
    """ Handle getting data from a GeoJSON file """

    geojson_layer_config = get_clean_config(layer_config, layer_name)
    add_tippecanoe_config(geojson_path, geojson_layer_config)
    return geojson_path


def handle_shapefile(shp_path, layer_name, layer_config, database_insert):
    """ Handle getting data from a shapefile """

    geojson_layer_config = get_clean_config(layer_config, layer_name)

    if database_insert:
        DB_VARS = os.environ
        shapefile2postgis(shp_path, layer_name, DB_VARS)
        postgis2geojson(layer_name, DB_VARS, LAYER_CONFIG=geojson_layer_config, QUERY=False)

    else:
        shapefile2geojson(shp_path, layer_name, LAYER_CONFIG=geojson_layer_config)

    return "/tiler-data/geojson/{}.geojson".format(layer_name)


def handle_gml(gml_path, layer_name, layer_config, database_insert):
    """ Handle getting data from a GML file """

    geojson_layer_config = get_clean_config(layer_config, layer_name)

    if database_insert:
        DB_VARS = os.environ
        shapefile2postgis(gml_path, layer_name, DB_VARS)
        postgis2geojson(layer_name, DB_VARS, LAYER_CONFIG=geojson_layer_config, QUERY=False)

    else:
        gml2geojson(gml_path, layer_name, LAYER_CONFIG=geojson_layer_config)

    return "/tiler-data/geojson/{}.geojson".format(layer_name)


if __name__ == '__main__':

    print "\n Checking input variables are valid..."

    if len(sys.argv) > 1:
        CONFIG = sys.argv[1]
    else:
        raise ValueError("Config file has not been defined")

    CONFIG_FILE = "/tiler-data/configs/" + CONFIG + ".tiler.json"
    tiles_from_config(CONFIG_FILE)
    