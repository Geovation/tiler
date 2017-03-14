from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

class TestHandler(BaseHTTPRequestHandler):

    #Handler for the GET requests
    def do_GET(self):

        send_reply = False
        if self.path.endswith(".zip"):
            mimetype = 'application/zip'
            send_reply = True

        if self.path.endswith(".json") or self.path.endswith(".geojson"):
            mimetype = 'application/json'
            send_reply = True
            
        if send_reply == True:
            #Open the static file requested and send it
            f = open(self.path)
            self.send_response(200)
            self.send_header('Content-Length', 999999) # TODO: do this properly
            self.send_header('Content-type', mimetype)
            self.end_headers()
            self.wfile.write(f.read())
            f.close()
            
        return
        # raise TypeError("Something went wrong")
 
