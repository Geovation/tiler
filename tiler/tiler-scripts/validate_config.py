import json
import sys
import os

def validate_config(name):

    config_path = "/tiler-data/configs/" + name + ".tiler.json"

    with open(config_path, 'r') as config_file:
        config_dump = config_file.read()
        config = json.loads(config_dump)
        for key in config["data"]:
            layer = config["data"][key]
            for path in layer["paths"]:
                if not os.path.isfile(path):
                    raise OSError("Config is not valid, path does not exist : " + path)

                if layer["type"] == "shapefile" and not path.endswith(".shp"):
                    raise OSError("File does not have shapefile extension but was marked as shapefile")
                    
                else:
                    print path, "is a valid file"
    
    print "Config", name, "is valid! :)"
    return True

if __name__ == '__main__':

    ## Check all our variables are in order
    if len(sys.argv) > 1:
        NAME = sys.argv[1]
    else:
        raise  ValueError("Config name not defined")

    validate_config(NAME)
