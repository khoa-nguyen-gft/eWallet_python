from entities.Accounts import Accounts, AccountType
from service.accountServices import save_account


def addNewMerchant(merchantName, merchantUrl):
    return save_account(Accounts(merchantName, AccountType.MERCHANT, 0, merchantUrl))