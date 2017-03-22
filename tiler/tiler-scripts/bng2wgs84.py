import subprocess
import sys
import os
from tiler_helpers import absolute_file_paths

def bng2wgs84(file_path, out_path):
    """Convert a shapefiles coordinate reference system from British National Grid to WGS84"""

    gsb = "/tiler-scripts/bin/OSTN02_NTv2.gsb"
    if not os.path.isfile(gsb):
        raise OSError("OSTN02_NTv2.gsb not found at : " + gsb)

    print "\n Commencing conversion from BNG to WGS84 using OSTN02: ", file_path
    command = 'ogr2ogr -s_srs "+proj=tmerc +lat_0=49 +lon_0=-2 +k=0.999601 \
               +x_0=400000 +y_0=-100000 +ellps=airy +units=m +no_defs +nadgrids={}" \
               -t_srs EPSG:4326 {} {}'.format(gsb, out_path, file_path)

    print "\n Running: ", command
    wgs84_process = subprocess.Popen(command, shell=True)
    exit_code = wgs84_process.wait()
    _, stderr = wgs84_process.communicate()
    if stderr:
        raise IOError(stderr)
    if exit_code != 0:
        raise IOError("Exit code was not 0 for bng2wgs84 process")

def convert_file(directory, file_path):
    """Run the British National Grid to WGS84 conversion to seperate file with a WGS84 extension"""

    if file_path.endswith(".shp"):
        base = os.path.basename(file_path)
        noext = os.path.splitext(base)[0]
        out_path = directory + "/" + noext + "_WGS84.shp"
        bng2wgs84(file_path, out_path)

def convert_folder(directory):
    """Convert a folder of shapefiles from British National Grid to WGS84"""

    for file_path in absolute_file_paths(directory):
        convert_file(directory, file_path)


if __name__ == '__main__':

    if len(sys.argv) > 1:
        INPUT_DIR = sys.argv[1]
    else:
        raise ValueError("INPUT_PATH not defined")

    convert_folder(INPUT_DIR)
    