#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
from json import dumps

from queue_client import QueueClient
from task import Task


class Proxy(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.client = QueueClient()
        super().__init__(*args, **kwargs)

    def _send_json(self, obj, status=200):
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(dumps(obj).encode("utf-8"))

    def do_POST(self):
        # Client -> envoie une Task
        content_length = int(self.headers.get("content-length", "0"))
        content = self.rfile.read(content_length).decode("utf-8")

        task = Task.from_json(content)
        self.client.task_queue.put(task)

        self._send_json({"status": "queued", "id": task.identifier})

    def do_GET(self):
        # Client <- récupère une Task calculée
        task = self.client.result_queue.get()
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(task.to_json().encode("utf-8"))

    def log_message(self, format, *args):
        print("[HTTP]", self.address_string(), "-", format % args)


def run():
    server_address = ("", 8000)
    httpd = HTTPServer(server_address, Proxy)
    print("Proxy listening on http://127.0.0.1:8000")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
