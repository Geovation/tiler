import subprocess
import sys

def geojson_extent():

    # TODO: Make grep Python level for interop
    process = subprocess.Popen('ogrinfo -ro -so -al {} | grep "Extent:"'.format(FILE_NAME), shell=True, stdout=subprocess.PIPE)
    for line in iter(process.stdout.readline,''):
    extent = line.rstrip()

    extent = extent.replace("Extent: ", "")
    extent = extent.replace("(", "").replace(")", "").replace(" - ", ", ")
    extent = "[" + extent + "]"
    return extent


if __name__ == '__main__':

    ## Check all our variables are in order
    if len(sys.argv) > 1:
        FILE_NAME = sys.argv[1]
    else:
        raise  ValueError("FILE_NAME not defined")
