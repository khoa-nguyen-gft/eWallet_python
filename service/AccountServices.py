import decimal

from entities import Accounts
from repository.AccountRepository import save, get_by_id, get_by_id_and_account_type, update
from service.TokenService import generate_token, verify_token

accounts_table = 'db/accounts.json'


def save_account(account: Accounts) -> Accounts:
    return save(account)


def generate_account_token(accountId: str) -> str:
    account = get_by_id(accountId)

    if account is not None:
        return generate_token(account.get('account_id'), account.get('account_type'))
    else:
        # Account not found
        print("Account not found: ", accountId)


def add_topup_account(accountId, token, amount):
    decoded_token = verify_token(token)
    print("decoded_token: ", decoded_token)

    # check the token is the issue banking
    bankIssue = get_by_id_and_account_type(decoded_token['accountId'], Accounts.AccountType.ISSUER)
    if bankIssue is not None:
        person = get_by_id(accountId)
        if person is not None:
            person['balance'] = float(decimal.Decimal(person['balance']) + decimal.Decimal(amount))
            print("person:", person)
            return update(person)
    else:
        return None