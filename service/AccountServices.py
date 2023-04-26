import decimal

from entities import Accounts
from repository.AccountRepository import (
    saveAccount,
    getAccountById,
    updateAccount
)
from service.TokenService import (
    generateToken,
    getIssueAccountByToken
)

accounts_table = 'db/accounts.json'


def save_account(account: Accounts) -> Accounts:
    return saveAccount(account)


def generate_account_token(accountId: str) -> str:
    account = getAccountById(accountId)

    if account is not None:
        return generateToken(account.get('account_id'), account.get('account_type'))
    else:
        # Account not found
        print("Account not found: ", accountId)


def add_topup_account(accountId, token, amount):
    # check the token is the issue banking
    bankIssue = getIssueAccountByToken(token)
    if bankIssue is not None:
        person = getAccountById(accountId)
        if person is not None:
            person['balance'] = float(decimal.Decimal(person['balance']) + decimal.Decimal(amount))
            print("person:", person)
            return updateAccount(person)
    else:
        return None
