import time

import jwt

from repository.AccountRepository import get_by_id_and_account_type

# Define the secret key and token expiration time
secret_key = 'mysecretkey'
token_expiration_time = 3600  # in seconds


# Function to generate a token
def generate_token(account_id, account_type):
    # Define the payload for the token
    payload = {'accountId': account_id, 'accountType': account_type, 'exp': int(time.time()) + token_expiration_time}

    # Set the token expiration time (1 hour from now)
    print("payload:", payload)

    # Generate the token using the JWT library
    token = jwt.encode(payload, secret_key, algorithm='HS256')

    # Return the token as a string
    return token.encode('utf-8').decode('ascii')


def verify_token(token):
    try:
        return jwt.decode(token, secret_key, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        # Handle case where token has expired
        return None
    except jwt.InvalidTokenError:
        # Handle case where token is invalid or malformed
        return None


def get_account_by_token_and_type(token: str, account_type: str) -> dict:
    decoded_token = verify_token(token)
    print("decoded_token: ", decoded_token, "token: ", token)
    if decoded_token is not None:
        return get_by_id_and_account_type(decoded_token['accountId'], account_type)