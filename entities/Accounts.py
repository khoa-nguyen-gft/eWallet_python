import uuid


class AccountType:
    PERSONAL = 'personal'
    MERCHANT = 'merchant'
    ISSUER = 'issuer'


# Account model
class Accounts:
    def __init__(self, account_name, account_type=AccountType.PERSONAL, balance_value=0):
        self.account_id = str(uuid.uuid4())
        self.account_name = account_name
        self.balance = balance_value
        self.account_type = account_type
