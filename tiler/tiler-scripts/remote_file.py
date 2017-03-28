import urllib2
import os
import zipfile
import sys
import traceback


def is_url(url):
    """ Check if a string is a valid URL """
    if url.startswith("http://") or url.startswith("https://"):
        return True
    return False

def is_zipfile(path):
    """ Check if a file is a zip file """
    if path.endswith(".zip"):
        return True
    return False

def download(url, output_dir):
    """ Download a file from a given URL to a specified directory """

    print "\n Downloading ", url
    if not is_url(url):
        raise TypeError("This does not appear to be a valid URL")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    file_name = os.path.join(output_dir, url.split('/')[-1])
    u = urllib2.urlopen(url)
    f = open(file_name, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes: %s" % (file_name, file_size)

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)
        print status,

    f.close()

    return file_name

def unzip(zip_file, output_dir):
    zfile = zipfile.ZipFile(zip_file)
    for name in zfile.namelist():
      (dirname, filename) = os.path.split(name)
      print "Decompressing " + filename + " on " + output_dir
      if not os.path.exists(output_dir):
        os.makedirs(output_dir)
      zfile.extract(name, output_dir)
