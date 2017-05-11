import os
import shutil
import mapbox_vector_tile
from tiler_helpers import absolute_file_paths 

def get_num_pbfs(src_dir):
    """ Get the number of vector tile protobufs in a folder recursively """

    return len([f for f in absolute_file_paths(src_dir) if f.endswith("pbf")])

def merge_tile_directories(src_dir1, src_dir2, root_dst_dir):
    """ Merge to vector tile directories, source into a destination directory """

    copy_dir(src_dir1, root_dst_dir)
    copy_dir(src_dir2, root_dst_dir)


def copy_dir(root_src_dir, root_dst_dir):
    """ Copy vector tiles from source to destination directory with overlap handling"""

    for src_dir, dirs, files in os.walk(root_src_dir):
        dst_dir = src_dir.replace(root_src_dir, root_dst_dir, 1)

        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        for file_ in files:
            src_file = os.path.join(src_dir, file_)
            dst_file = os.path.join(dst_dir, file_)
            if os.path.exists(dst_file):                
                # If we have .pbf's that clash, we want to merge them 
                # together and write them to the new directory as dst_dir

                if file_ == "metadata.json":
                    os.remove(dst_file)
                else:
                    print "\n Merging tiles to... " + dst_file

                    with open(src_file, 'rb') as f:
                        data = f.read()
                    decoded_data1 = mapbox_vector_tile.decode(data)

                    with open(dst_file, 'rb') as f:
                        data = f.read()
                    decoded_data2 = mapbox_vector_tile.decode(data)
                    
                    for k, v in decoded_data2.items():
                        if k in decoded_data1:
                            decoded_data1[k]["features"] += decoded_data2[k]["features"]
                        else:
                            decoded_data1[k] = decoded_data2[k]                       

                    listofdict = []
                    for k, v in decoded_data1.items():
                        dic = {
                            'name': k,
                            'features': decoded_data1[k]["features"]
                        }
                        listofdict.append(dic)

                    encoded_data = mapbox_vector_tile.encode(listofdict)
                    with open(dst_file, 'w') as f:
                        f.write(encoded_data)
            else:                
                shutil.copy(src_file, dst_dir)