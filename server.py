from service.AccountServices import accounts_table, add_topup_account, generate_account_token, save_account
from service.MerchantService import addNewMerchant
from email.message import EmailMessage
from http.server import BaseHTTPRequestHandler, HTTPServer

from entities.Accounts import Accounts
from pysondb import db
import os
import re
import json

from service.TransactionService import create_transaction, cancel_transaction, confirm_transaction


def _parse_header(content_type):
    m = EmailMessage()
    m['content-type'] = content_type
    return m.get_content_type(), m['content-type'].params


class HTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print("Get path: ", self.path)
        if self.path.startswith('/hello'):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            message = {'message': 'Hello, world!'}
            self.wfile.write(json.dumps(message).encode())

        if self.path.startswith('/account/'):
            path_parts = self.path.split('/')
            if path_parts[1] == 'account' and path_parts[3] == 'token':
                account_id = path_parts[2]
                print("account_id:", account_id)

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()

                token = generate_account_token(account_id)
                if token is not None:
                    # Construct the response JSON and send it back to the client
                    response = {
                        'accountId': account_id,
                        'token': token
                    }
                    self.wfile.write(json.dumps(response).encode())
                else:
                    self.send_response(404)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    message = {'message': 'Not Found'}
                    self.wfile.write(json.dumps(message).encode())
            else:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                message = {'message': 'Not Found'}
                self.wfile.write(json.dumps(message).encode())

    def do_POST(self):
        print("Post path: ", self.path)
        if re.search('/merchant/signup/*', self.path):
            if self.headers.get('content-type') == 'application/json':
                length = int(self.headers.get('content-length'))
                bodyStr = self.rfile.read(length).decode('utf8')
                jsonObj = json.loads(bodyStr)
                print("Body content: ", jsonObj)
                newMerchant = addNewMerchant(jsonObj["merchantName"], jsonObj["merchantUrl"])
                jsonStr = json.dumps(newMerchant)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(jsonStr.encode(encoding='utf_8'))
            else:
                self.send_response(400, "Bad Request: invalid data")
                self.end_headers()
        if self.path.startswith('/account/'):
            path_parts = self.path.split('/')
            if path_parts[1] == 'account' and path_parts[3] == 'topup':
                if self.headers.get('content-type') == 'application/json':
                    account_id = path_parts[2]
                    auth_token = self.headers.get('Authentication')

                    if auth_token is None:
                        self.authTokenResponse()
                        return

                    content_length = int(self.headers.get('Content-Length', 0))
                    jsonObj = json.loads(self.rfile.read(content_length))

                    result = add_topup_account(account_id, auth_token, jsonObj['amount'])
                    jsonStr = json.dumps(result)

                    print("result", result)
                    if result is None:
                        return self.ErrorUnAuthentication()

                    # Validate payload schema using the TopupRequest definition
                    # Return a successful response
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(jsonStr.encode(encoding='utf_8'))

        if self.path == '/account':
            if self.headers.get('content-type') == 'application/json':
                length = int(self.headers.get('content-length'))
                bodyStr = self.rfile.read(length).decode('utf8')
                jsonObj = json.loads(bodyStr)
                print("Body content: ", jsonObj)
                account = save_account(Accounts(jsonObj["accountName"], jsonObj["accountType"]))
                jsonStr = json.dumps(account)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(jsonStr.encode(encoding='utf_8'))
            else:
                self.send_response(400, "Bad Request: invalid data")
                self.end_headers()
        if self.path.startswith('/transaction'):
            path_parts = self.path.split('/')

            auth_token = self.headers.get('Authentication')

            if auth_token is None:
                self.authTokenResponse()
                return
            content_length = int(self.headers.get('Content-Length', 0))
            jsonStr = json.loads(self.rfile.read(content_length))
            result = None

            if path_parts[2] == 'create':
                result = create_transaction(auth_token, jsonStr)

            elif path_parts[2] == 'confirm':
                result = confirm_transaction(auth_token, jsonStr)

            elif path_parts[2] == 'verify':
                result = create_transaction(auth_token, jsonStr)

            elif path_parts [2] == 'cancel':
                result = cancel_transaction(auth_token, jsonStr)

            print("result", result)
            if result is None:
                return self.ErrorUnAuthentication()

            # Validate payload schema using the TopupRequest definition
            # Return a successful response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write("passed".encode(encoding='utf_8'))

    def authTokenResponse(self):
        self.send_response(400, "Bad Request: invalid data")
        self.end_headers()
        response_body = json.dumps({"message": "Account is not Authentication"})
        self.wfile.write(response_body.encode('utvf-8'))

    def ErrorUnAuthentication(self):
        self.authTokenResponse()
        return


def main():
    initDataBase()
    server = HTTPServer(("localhost", 8080), HTTPRequestHandler)
    print('HTTP Server Running...........')
    server.serve_forever()


def initDataBase():
    if not os.path.exists(accounts_table):
        db.getDb(accounts_table)


if __name__ == '__main__':
    main()
