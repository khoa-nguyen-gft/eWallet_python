from email.message import EmailMessage
from http.server import BaseHTTPRequestHandler, HTTPServer
from service import merchantService
from pysondb import db
import os
import re
import json

merchant_table = 'db/merchant.json'


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

    def do_POST(self):
        if re.search('/merchant/signup/*', self.path):
            if self.headers.get('content-type') == 'application/json':
                length = int(self.headers.get('content-length'))
                bodyStr = self.rfile.read(length).decode('utf8')
                jsonObj = json.loads(bodyStr)
                print("Body content: ", jsonObj)
                newMerchant = merchantService.addNewMerchant(jsonObj["merchantName"], jsonObj["merchantUrl"])
                jsonStr = json.dumps(newMerchant)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(jsonStr.encode(encoding='utf_8'))
            else:
                self.send_response(400, "Bad Request: invalid data")
                self.end_headers()


def main():
    initDataBase()
    server = HTTPServer(("localhost", 8080), HTTPRequestHandler)
    print('HTTP Server Running...........')
    server.serve_forever()


def initDataBase():
    if not os.path.exists(merchant_table):
        db.getDb(merchant_table)


if __name__ == '__main__':
    main()
