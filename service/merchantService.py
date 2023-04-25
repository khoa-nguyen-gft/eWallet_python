from pysondb import db
from uuid import uuid4

merchant_table = 'db/merchant.json'


def addNewMerchant(merchantName, merchantUrl):
    merchants = db.getDb(merchant_table)
    newMerchant = {
        "accountId": str(uuid4()),
        "merchantId": str(uuid4()),
        "merchantName": merchantName,
        "merchantUrl": merchantUrl,
        "apiKey": str(uuid4())
    }
    merchants.add(newMerchant)
    return newMerchant
