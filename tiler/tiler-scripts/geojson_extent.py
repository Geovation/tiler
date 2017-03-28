import subprocess
import sys
import os
from itertools import tee

def geojson_extent(FILE_NAME):
    """Get the geographic extent of a GeoJSON file in WGS84"""

    # TODO: Make grep Python level for interop
    assert os.path.isfile(FILE_NAME)
    command = 'ogrinfo -ro -so -al {} | grep "Extent:"'.format(FILE_NAME)
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)

    lines = iter(process.stdout.readline, '')
    lines_sum = tee(lines) # We need to copy the iterator!
    if sum(1 for _ in lines_sum) == 0:
        raise OSError("There was no extent information for this file")

    for line in lines:
        extent = line.rstrip()

    extent = extent.replace("Extent: ", "")
    extent = extent.replace("(", "").replace(")", "").replace(" - ", ", ")
    extent = [float(x) for x in extent.split(",")]
    return extent


if __name__ == '__main__':

    ## Check all our variables are in order
    if len(sys.argv) > 1:
        FILE_NAME = sys.argv[1]
        EXTENT = geojson_extent(FILE_NAME)
        print EXTENT
    else:
        raise ValueError("FILE_NAME not defined")