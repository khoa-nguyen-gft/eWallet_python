from pysondb import db
from entities import Accounts
from service.TokenService import generate_token, verify_token

accounts_table = 'db/accounts.json'


def save_account(account: Accounts) -> Accounts:
    accounts = db.getDb(accounts_table)

    entity = {
        "account_id": account.account_id,
        "account_name": account.account_name,
        "balance": account.balance,
        "account_type": account.account_type,
        'url': account.url
    }

    accounts.add(entity)
    return entity


def generate_account_token(accountId: str) -> str:
    accounts = db.getDb(accounts_table)

    # Loop through the accounts in the database
    print(accounts.getAll())
    for account in accounts.getAll():
        # Check if the account ID matches
        if account.get('account_id') == accountId:
            # Found the account, do something with it
            return generate_token(account.get('account_id'), account.get('account_type'))
    else:
        # Account not found
        print("Account not found: ", accountId)


def add_topup_account(accountId, token, amount):
    decoded_token = verify_token(token, accountId)
    if decoded_token is not None:
        # TODO process business logic
        print("decoded_token:", decoded_token)
        print("accountId:", accountId)
        print("amount:", amount)

        return accountId
    else:
        return None
