import * from globalmaptiles

def lat_lon_to_tile(x, y):
    lat, lon = LatLonToMeters(x, y)
    return MetersToTile(lat, lon, 18)

def get_tile_bounding_box(max_x, max_y, min_x, min_y):

    MAX_TILE_ZOOM = 18

    top, right = lat_lon_to_tile(max_x, max_y)
    bottom, left = lat_lon_to_tile(min_x, min_y)
    bottom_left_bounds = TileLatLonBounds(bottom, left, MAX_TILE_ZOOM)
    top_right_bounds = TileLatLonBounds(bottom, left, MAX_TILE_ZOOM)

    #minLat, minLon, maxLat, maxLon
    bottom_left_bounds = [bottom_left_bounds[0], bottom_left_bounds[1]]
    top_right_bounds = [top_right_bounds[0], top_right_bounds[1]]

    return [bottom_left_bounds, top_right_bounds]

def generate_changed_tiles(layers, simplifcation, changes_bounding_box, geometry_column, layers):

    # config = {
    #     "layername" : {
    #         "minzoom" : 3,
    #         "maxzoom" : 10
    #     }
    # }

    # Get the parts in WGS84 from the bounding box of all geographic changes
    min_x = changes_bounding_box[0]
    min_y = changes_bounding_box[1]
    max_x = changes_bounding_box[2]
    max_y = changes_bounding_box[3]

    # Get the bounding box using the tile buffer region
    bounding_box = get_tile_bounding_box(max_x, max_y, min_x, min_y)

    # Create a Bounding Box that PostGIS can understand
    bounding_box_sql = "ST_MakeEnvelope ({}, {}, {}, {}, 4326)".format(
        bounding_box[0][0], 
        bounding_box[0][1], 
        bounding_box[1][0],
        bounding_box[1][1] 
    )

    sql = "SELECT * FROM {} WHERE ST_Intersects({}, {})".format(
        layer_name,
        geometry_column,
        bounding_box_sql
    )

    data = {}
    for layer in layers.iterkeys():
        layers[layer]["type"] = "postgis"
        layers[layer]["query"] = sql
            "type" : "postgis",
            "query" : sql,
            "minzoom" : 
            "maxzoom" : 14
        }

    update_config = {
        "outdir" : "/tiler-data/tiles/",
        "tileset" : name,
        "simplification" : 5,
        "data" : data
    }
    
    

def update_changed_tiles():
    pass

