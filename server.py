import json
import logging
import os
import re
from email.message import EmailMessage
from http.server import BaseHTTPRequestHandler, HTTPServer

from pysondb import db

from service.AccountServices import (
    accounts_table,
    add_topup_account,
    generate_account_token,
    save_account,
)
from service.MerchantService import addNewMerchant
from service.TransactionService import (
    cancel_transaction,
    confirm_transaction,
    create_transaction,
    verify_transaction,
)
from entities.Accounts import Accounts


def _parse_header(content_type):
    m = EmailMessage()
    m['content-type'] = content_type
    return m.get_content_type(), m['content-type'].params


class HTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        logging.info(f"GET path: {self.path}")
        if self.path.startswith("/hello"):
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            message = {"message": "Hello, world!"}
            self.wfile.write(json.dumps(message).encode())

        if self.path.startswith("/account/"):
            path_parts = self.path.split("/")
            if path_parts[1] == "account" and path_parts[3] == "token":
                account_id = path_parts[2]
                logging.info(f"account_id: {account_id}")

                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()

                token = generate_account_token(account_id)
                if token is not None:
                    # Construct the response JSON and send it back to the client
                    response = {"accountId": account_id, "token": token}
                    self.wfile.write(json.dumps(response).encode())
                else:
                    self.send_response(404)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    message = {"message": "Not Found"}
                    self.wfile.write(json.dumps(message).encode())
            else:
                self.send_response(404)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                message = {"message": "Not Found"}
                self.wfile.write(json.dumps(message).encode())

    def do_POST(self):
        logging.info(f"POST path: {self.path}")
        if re.search("/merchant/signup/*", self.path):
            if self.headers.get("content-type") == "application/json":
                length = int(self.headers.get("content-length"))
                body_str = self.rfile.read(length).decode("utf8")
                json_obj = json.loads(body_str)
                logging.info(f"Body content: {json_obj}")
                new_merchant = addNewMerchant(
                    json_obj["merchantName"], json_obj["merchantUrl"]
                )
                json_str = json.dumps(new_merchant)
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json_str.encode(encoding="utf_8"))

        if self.path.startswith('/account'):
            path_parts = self.path.split('/')
            accountId = None
            if len(path_parts) >= 3 and path_parts[1] == "account":
                accountId = path_parts[2]
            print("path_parts", path_parts)
            print("accountId", accountId)

            if accountId is None:
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
            elif accountId is not None and path_parts[3] == 'topup':
                if self.headers.get('content-type') == 'application/json':
                    account_id = path_parts[2]
                    auth_token = self.headers.get('Authentication')

                    if auth_token is None:
                        self.authTokenResponse()
                        return

                    content_length = int(self.headers.get('Content-Length', 0))
                    jsonObj = json.loads(self.rfile.read(content_length))

                    result = add_topup_account(account_id, auth_token, jsonObj['amount'])
                    if result is None:
                        return self.ErrorUnAuthentication()

                    jsonStr = json.dumps(result)
                    print("result", result)

                    # Validate payload schema using the TopupRequest definition
                    # Return a successful response
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(jsonStr.encode(encoding='utf_8'))

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
                print("start processing create transaction: ", jsonStr)
                result = create_transaction(auth_token, jsonStr)

            elif path_parts[2] == 'verify':
                print("start processing verify  transaction: ", jsonStr)
                result = verify_transaction(auth_token, jsonStr['transactionId'])

            elif path_parts[2] == 'confirm':
                print("start processing confirm transaction: ", jsonStr)
                result = confirm_transaction(auth_token, jsonStr['transactionId'])

            elif path_parts[2] == 'cancel':
                print("start processing cancel transaction: ", jsonStr)
                result = cancel_transaction(auth_token,  jsonStr['transactionId'])

            print("result", result)
            if result is None:
                return self.ErrorUnAuthentication()

            # Validate payload schema using the TopupRequest definition
            # Return a successful response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())

    def ErrorUnAuthentication(self):
        self.send_response(401, "Unauthorized: invalid authentication credentials")
        self.end_headers()
        return

    def authTokenResponse(self):
        self.send_response(401, "Unauthorized: no authentication credentials provided")
        self.end_headers()
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
