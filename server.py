from email.message import EmailMessage
from http.server import BaseHTTPRequestHandler, HTTPServer
import json


def _parse_header(content_type):
    m = EmailMessage()
    m['content-type'] = content_type
    return m.get_content_type(), m['content-type'].params


class HTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/hello':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            message = {'message': 'Hello, world!'}
            self.wfile.write(json.dumps(message).encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            message = {'message': 'Not Found'}
            self.wfile.write(json.dumps(message).encode())


def main():
    server = HTTPServer(("localhost", 8080), HTTPRequestHandler)
    print('HTTP Server Running...........')
    server.serve_forever()


if __name__ == '__main__':
    main()
