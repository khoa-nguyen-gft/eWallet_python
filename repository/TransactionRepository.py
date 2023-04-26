from pysondb import db

transaction_table = 'db/transactions.json'


def saveTransaction(entity):
    transactions = db.getDb(transaction_table)
    transactions.add(entity)
    return entity


def updateTransaction(entity):
    transactions = db.getDb(transaction_table)
    transactions.updateById(entity["id"], entity)
    return entity


def getTransactionAll():
    accounts = db.getDb(transaction_table)
    return accounts.getAll()


def getTransactionById(transactionId: str):
    transactions = db.getDb(transaction_table)

    for transaction in transactions.getAll():
        # Check if the account ID matches
        if transaction.get('transaction_id') == transactionId:
            # Found the account, do something with it
            return transaction
    else:
        return None

