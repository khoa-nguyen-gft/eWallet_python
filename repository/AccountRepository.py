from pysondb import db
from entities import Accounts

accounts_table = 'db/accounts.json'


def saveAccount(account: Accounts) -> Accounts:
    accounts = db.getDb(accounts_table)

    entity = {
        "account_id": account.account_id,
        "account_name": account.account_name,
        "balance": account.balance,
        "credit": "0",
        "account_type": account.account_type,
        'url': account.url
    }
    accounts.add(entity)
    return entity


def updateAccount(account):
    accounts = db.getDb(accounts_table)
    accounts.updateById(account["id"], account)
    return account


def getAccountAll():
    accounts = db.getDb(accounts_table)
    return accounts.getAll()


def getAccountById(accountId: str):
    accounts = db.getDb(accounts_table)

    for account in accounts.getAll():
        # Check if the account ID matches
        if account.get('account_id') == accountId:
            # Found the account, do something with it
            return account
    else:
        return None


def getAccountByIdAndAccountType(accountId, accountType):
    accounts = db.getDb(accounts_table)
    for account in accounts.getAll():
        if account.get("account_id") == accountId and account.get("account_type") == accountType:
            return account
    else:
        return None
