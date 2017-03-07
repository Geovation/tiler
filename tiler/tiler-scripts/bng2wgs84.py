import subprocess
import sys
import os
from tiler_helpers import absolute_file_paths

def bng2wgs84(FILE_PATH, OUT_PATH):

    GSB = "/tiler-scripts/bin/OSTN02_NTv2.gsb"
    if not os.path.isfile(GSB):
        raise OSError("OSTN02_NTv2.gsb not found at : " + GSB)

    print "\n Commencing conversion from BNG to WGS84 using OSTN02: ", FILE_PATH
    command = 'ogr2ogr -s_srs "+proj=tmerc +lat_0=49 +lon_0=-2 +k=0.999601 +x_0=400000 +y_0=-100000 +ellps=airy +units=m +no_defs +nadgrids={}" -t_srs EPSG:4326 {} {}'.format(GSB, OUT_PATH, FILE_PATH)
    print "\n Running: ", command
    wgs84_process = subprocess.Popen(command, shell=True)
    exit_code = wgs84_process.wait()
    stdout, stderr = wgs84_process.communicate()
    if stderr:
        raise IOError(sterr)
    if exit_code != 0:
        raise IOError("Exit code was not 0 for bng2wgs84 process")

def convert_file(DIRECTORY, FILE_PATH):
    if FILE_PATH.endswith(".shp"):
        base = os.path.basename(FILE_PATH)
        noext = os.path.splitext(base)[0]
        out_path = DIRECTORY + "/" + noext + "_WGS84.shp"
        bng2wgs84(FILE_PATH, out_path)

def convert_folder(directory):
    for file_path in absolute_file_paths(directory):
        convert_file(directory, file_path)


if __name__ == '__main__':

    if len(sys.argv) > 1:
        INPUT_DIR = sys.argv[1]
    else:
        raise  ValueError("INPUT_PATH not defined" )
    
    convert_folder(INPUT_DIR)
    