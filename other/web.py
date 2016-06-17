#!/usr/bin/python3

from http.server import BaseHTTPRequestHandler
from http.cookies import SimpleCookie
import socketserver
import urllib
import uuid

class JeopardyHTTPHandler(BaseHTTPRequestHandler):
    _id_mapping = {}

    def __init__(self, *args, **kwargs):

        super(JeopardyHTTPHandler, self).__init__(*args, **kwargs)

    def do_GET(self):
        client_id = self._get_client_id()

        self.send_response(200)

        # set cookie if necessary
        if not client_id:
            client_id = self._generate_client_id()
            JeopardyHTTPHandler._id_mapping[client_id] = 0
            self._set_client_id(client_id)

        self.send_header("Content-type", "text/html")
        self.end_headers()

        with open('index.html', 'rb') as f:
            for line in f.readlines():
                self.wfile.write(line)

    def do_POST(self):
        client_id = self._get_client_id()

        if client_id:
            print("Buzzer: " + client_id)
            self.send_response(200)
        else:
            self.send_response(400)
        self.end_headers()

    def _get_client_id(self):
        if "Cookie" in self.headers:
            c = SimpleCookie(self.headers["Cookie"])
            if 'id' in c:
                client_id = c['id'].value
                if client_id in JeopardyHTTPHandler._id_mapping:
                    return c['id'].value

        return None

    def _set_client_id(self, client_id):
        c = SimpleCookie()
        c['id'] = client_id
        self.send_header('Set-Cookie', c.output(header=''))

    def _generate_client_id(self):
        client_id = uuid.uuid4()

        while client_id in JeopardyHTTPHandler._id_mapping:
            client_id = uuid.uuid4()

        return client_id.hex

class Webserver:
    def __init__(self):
        #super(Webserver, self).__init__("Webserver")

        self.configdialog = None

        self._callback = None

        #for key in range(1, 51):
        #    self.all_keys[key] = str(key)

        socketserver.TCPServer.allow_reuse_address = True

        self._httpd = None

    def connect(self):
        self._httpd = socketserver.TCPServer(("", 8080), JeopardyHTTPHandler)

        self._httpd.serve_forever()

    def disconnect(self):
        if self._httpd:
            self._httpd.shutdown()

    def start(self, callback):
        pass

    def stop(self):
        pass

server = Webserver()
server.connect()
