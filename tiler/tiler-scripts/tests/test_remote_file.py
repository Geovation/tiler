import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Insanity for getting parent folder in path
from remote_file import *
import SocketServer
import threading
from handler import TestHandler


class TestShapefile2Geojson(unittest.TestCase):

    def test_is_url(self):
        self.assertFalse(is_url("not_a_url"))
        self.assertTrue(is_url("http://www.geovation.uk"))

    def test_is_zip(self):
        self.assertFalse(is_zipfile("not_a_zip_file"))
        self.assertTrue(is_zipfile("/tiler-data/test-data/test.zip"))

    def test_download(self):
 
        PORT = 8080
        SocketServer.TCPServer.allow_reuse_address = True
        server = SocketServer.TCPServer(("", PORT), TestHandler)
        thread = threading.Thread(target = server.serve_forever)
        thread.daemon = True
        thread.start()
        download("http://localhost:" + str(PORT) + "/tiler-data/test-data/test.zip", "/tiler-data/input")
        self.assertTrue(os.path.isfile("/tiler-data/test-data/test.zip"))
        server.shutdown()
        server.socket.close()

    def test_unzip(self):
        self.assertTrue(os.path.isfile("/tiler-data/test-data/test.zip"))
        unzip("/tiler-data/test-data/test.zip", "/tiler-data/test-data/zip-output/")
        self.assertTrue(os.path.isfile("/tiler-data/test-data/zip-output/testzip/test"))

    def tearDown(self):
        pass
        try:
            print "\n Tearing tests down..."
            os.remove("/tiler-data/input/test.zip")
        except OSError as os_err:
            pass



if __name__ == '__main__':
    unittest.main()