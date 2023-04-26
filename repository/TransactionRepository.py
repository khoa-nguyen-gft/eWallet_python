from pysondb import db

transaction_table = 'db/transactions.json'


def save(transaction):
    transactions = db.getDb(transaction_table)

    entity = {
        "transaction_id": str(transaction.transactionId),
        "merchant_id": transaction.merchantId,
        "income_account": transaction.incomeAccount,
        "outcome_account": transaction.outcomeAccount,
        "amount": transaction.amount,
        "extra_data": transaction.extraData,
        "signature": transaction.signature,
        "status": transaction.status
    }

    transactions.add(entity)
    return entity


def update(transaction):
    transactions = db.getDb(transaction_table)
    transactions.updateById(transaction["id"], transaction)
    return transaction


def get_all():
    accounts = db.getDb(transaction_table)
    return accounts.getAll()


def get_by_id(transactionId: str):
    transactions = db.getDb(transaction_table)

    for transaction in transactions.getAll():
        # Check if the account ID matches
        if transaction.get('transaction_id') == transactionId:
            # Found the account, do something with it
            return transaction
    else:
        return None
