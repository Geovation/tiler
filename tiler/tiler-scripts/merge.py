
import os
import shutil
from tiler_helpers import absolute_file_paths 


def get_num_pbfs(src_dir):
    """ Get the number of vector tile protobufs in a folder recursively """

    return len([f for f in absolute_file_paths(src_dir) if f.endswith("pbf")])

def merge_tile_directories(root_src_dir, root_dst_dir, overwrite=False):
    """ Merge to vector tile directories, source into a destination directory. Optionally overwrite from the source """

    for src_dir, dirs, files in os.walk(root_src_dir):
        dst_dir = src_dir.replace(root_src_dir, root_dst_dir, 1)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        for file_ in files:
            src_file = os.path.join(src_dir, file_)
            dst_file = os.path.join(dst_dir, file_)
            if os.path.exists(dst_file):
                if overwrite or file_ == "metadata.json":
                    os.remove(dst_file)
                elif file_ != "metadata.json":
                    raise OSError("File already exists but overwrite was set to false: " + file_)
            shutil.move(src_file, dst_dir)
