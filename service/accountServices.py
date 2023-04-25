from pysondb import db
from entities import Accounts
from service.GenerateTokenService import generate_token

accounts_table = 'db/accounts.json'


def save_account(account: Accounts) -> Accounts:
    accounts = db.getDb(accounts_table)

    entity = {
        "account_id": account.account_id,
        "account_name": account.account_name,
        "balance": account.balance,
        "account_type": account.account_type,
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
