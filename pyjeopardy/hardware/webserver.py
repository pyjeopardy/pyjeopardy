#!/usr/bin/python3

from pyjeopardy.game import Hardware
from pyjeopardy.config import MEDIA_DIR, HARDWARE_POLLINTERVAL

from PyQt5 import QtCore

from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler
from queue import Queue

import os
import socketserver
import threading
import uuid


class Webserver(Hardware):
    _id_mapping = {}
    _next_key = 1
    _started = False
    _queue = Queue()

    def __init__(self):
        super(Webserver, self).__init__("Webserver")

        self.configdialog = None

        self._timer = QtCore.QTimer()
        self._timer.setInterval(HARDWARE_POLLINTERVAL)
        self._timer.timeout.connect(self.update)
        self._timer.start()

        self._callback = None

        for key in range(1, 51):
            self.all_keys[key] = str(key)

        socketserver.TCPServer.allow_reuse_address = True

        self._httpd = None
        self._thread = None

        Webserver._started = False

    def connect(self):
        self._httpd = socketserver.TCPServer(("", 8080), JeopardyHTTPHandler)

        self._thread = threading.Thread(target=self._httpd.serve_forever)
        self._thread.daemon = True
        self._thread.start()

    def disconnect(self):
        if self._httpd:
            self._httpd.shutdown()
            self._httpd = None

    def start(self, callback):
        Webserver._started = True
        self._callback = callback

    def stop(self):
        Webserver._started = False
        self._callback = None

    def update(self):
        if self.active and self._callback and not Webserver._queue.empty():
            self._callback(self, Webserver._queue.get())


class JeopardyHTTPHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):

        super(JeopardyHTTPHandler, self).__init__(*args, **kwargs)

    def do_GET(self):
        client_id = self._get_client_id()

        self.send_response(200)

        # set cookie if necessary
        if not client_id:
            client_id = self._generate_client_id()
            Webserver._id_mapping[client_id] = Webserver._next_key
            Webserver._next_key += 1
            self._set_client_id(client_id)

        self.send_header("Content-type", "text/html")
        self.end_headers()

        with open(os.path.join(MEDIA_DIR, 'webserver.html'), 'rb') as f:
            for line in f.readlines():
                self.wfile.write(line)

    def do_POST(self):
        client_id = self._get_client_id()

        if not Webserver._started:
            self.send_response(403)  # forbidden
        elif client_id:
            if Webserver._queue.empty():
                Webserver._queue.put(Webserver._id_mapping[client_id])
            self.send_response(200)
        else:
            self.send_response(400)  # bad request
        self.end_headers()

    def log_message(self, format, *args):
        return  # do not print log messages

    def _get_client_id(self):
        if "Cookie" in self.headers:
            c = SimpleCookie(self.headers["Cookie"])
            if 'id' in c:
                client_id = c['id'].value
                if client_id in Webserver._id_mapping:
                    return c['id'].value

        return None

    def _set_client_id(self, client_id):
        c = SimpleCookie()
        c['id'] = client_id
        self.send_header('Set-Cookie', c.output(header=''))

    def _generate_client_id(self):
        client_id = uuid.uuid4()

        while client_id in Webserver._id_mapping:
            client_id = uuid.uuid4()

        return client_id.hex
