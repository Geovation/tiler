from globalmaptiles import *
from tiler import handle_config

convert = GlobalMercator()

def lat_lon_to_tile(lat, lon, zoom):
    x, y = convert.LatLonToMeters(lat, lon)
    tx, ty = convert.MetersToTile(x, y, zoom)
    return tx, ty #convert.GoogleTile(tx, ty, zoom)

def get_tile_bounding_box(min_x, min_y, max_x, max_y, zoom):

    left, bottom = lat_lon_to_tile(min_y, min_x, zoom) #lat, lon
    right, top = lat_lon_to_tile(max_y, max_x, zoom) #lat, lon
    
    bottom_left_bounds = convert.TileLatLonBounds(left, bottom, zoom) #xy
    top_right_bounds = convert.TileLatLonBounds(right, top, zoom) #xy

    bottom_left_bounds = [bottom_left_bounds[0], bottom_left_bounds[1]]
    top_right_bounds = [top_right_bounds[2], top_right_bounds[3]]

    return [bottom_left_bounds, top_right_bounds]

def generate_changed_tiles(name, layers, simplifcation, changes_bounding_box, geometry_column):

    # Get the parts in WGS84 from the bounding box of all geographic changes
    min_x = changes_bounding_box[0]
    min_y = changes_bounding_box[1]
    max_x = changes_bounding_box[2]
    max_y = changes_bounding_box[3]

    # Get the bounding box using the tile buffer region
    bounding_box = get_tile_bounding_box(max_x, max_y, min_x, min_y, 18)

    # Create a Bounding Box that PostGIS can understand
    bounding_box_sql = "ST_MakeEnvelope ({}, {}, {}, {}, 4326)".format(
        bounding_box[0][0], 
        bounding_box[0][1], 
        bounding_box[1][0],
        bounding_box[1][1] 
    )

    for layer in layers["data"].iterkeys():
        layers["data"][layer]["type"] = "postgis"
        sql = "SELECT * FROM {} WHERE ST_Intersects({}, {})".format(
            layer,
            geometry_column,
            bounding_box_sql
        )
        layers["data"][layer]["query"] = sql

    handle_config(layers)





def update_changed_tiles():
    pass

