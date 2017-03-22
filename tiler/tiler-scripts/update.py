# from globalmaptiles import *
# from tiler import tiles_from_config
# import os
# import shutil


# convert = GlobalMercator()

# def lat_lon_to_tile(lat, lon, zoom):
#     x, y = convert.LatLonToMeters(lat, lon)
#     tx, ty = convert.MetersToTile(x, y, zoom)
#     return tx, ty #convert.GoogleTile(tx, ty, zoom)

# def get_tile_bounding_box(min_x, min_y, max_x, max_y, zoom):
#     # THIS RETURNS LAT, LNG BOUNDING BOXES 

#     left, bottom = lat_lon_to_tile(min_y, min_x, zoom) #lat, lon
#     right, top = lat_lon_to_tile(max_y, max_x, zoom) #lat, lon

#     bottom_left_bounds = convert.TileLatLonBounds(left, bottom, zoom) #xy
#     top_right_bounds = convert.TileLatLonBounds(right, top, zoom) #xy

#     bottom_left_bounds = [bottom_left_bounds[0], bottom_left_bounds[1]]
#     top_right_bounds = [top_right_bounds[2], top_right_bounds[3]]

#     return [bottom_left_bounds, top_right_bounds]


# def get_envelope_sql(changes_bounding_box):

#     # Get the parts in WGS84 from the bounding box of all geographic changes
#     # Reminder get_tile_bounding_box returns LAT LNG bounding boxes NOT LNG LAT!
#     min_x = changes_bounding_box[1]
#     min_y = changes_bounding_box[0]

#     max_x = changes_bounding_box[3]
#     max_y = changes_bounding_box[2]

#     # Get the bounding box using the tile buffer region
#     bounding_box = get_tile_bounding_box(min_x, min_y, max_x, max_y, 18)

#     # Create a Bounding Box that PostGIS can understand
#     bounding_box_sql = "ST_MakeEnvelope ({}, {}, {}, {}, 4326)".format(
#         bounding_box[0][0], 
#         bounding_box[0][1], 
#         bounding_box[1][0],
#         bounding_box[1][1] 
#     )

#     return bounding_box_sql 


# def generate_changed_tiles(layers, simplifcation, changes_bounding_box, geometry_column):

#     bounding_box_sql = get_envelope_sql(changes_bounding_box)

#     print "Bounding box sql: ", bounding_box_sql

#     for layer in layers["data"].iterkeys():
#         layers["data"][layer]["type"] = "postgis"
#         sql = "SELECT * FROM {} WHERE ST_Intersects({}, {})".format(
#             layer,
#             geometry_column,
#             bounding_box_sql
#         )
#         layers["data"][layer]["query"] = sql


#     print "Layers after generate tiles", layers

#     # import pdb;pdb.set_trace()

#     tiles_from_config(layers)

#     # import pdb;pdb.set_trace()

# # def get_effected_tiles(bounding_box):
    
    
# #     lat_lon_to_tile


# def update_tile_directories(root_src_dir, root_dst_dir):

#     for src_dir, dirs, files in os.walk(root_src_dir):
#         dst_dir = src_dir.replace(root_src_dir, root_dst_dir, 1)
#         if not os.path.exists(dst_dir):
#             os.makedirs(dst_dir)
#         for file_ in files:
#             src_file = os.path.join(src_dir, file_)
#             dst_file = os.path.join(dst_dir, file_)
#             if os.path.exists(dst_file):
#                 os.remove(dst_file)
#             shutil.move(src_file, dst_dir)
