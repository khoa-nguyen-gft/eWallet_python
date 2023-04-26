
from entities.Transaction import (
    intTransactionEntity,
    TransactionType
)
from repository.AccountRepository import getAccountById, updateAccount
from repository.TransactionRepository import (
    getTransactionById,
    saveTransaction,
    updateTransaction
)
from service.TokenService import (
    getMerchantAccountByToken,
    getPersonalAccountByToken
)


def create_transaction(auth_token, transactionCreateRequest):
    merchant = getMerchantAccountByToken(auth_token)
    print("merchant: ", merchant)
    print("transactionCreateRequest: ", transactionCreateRequest)
    if merchant is not None:
        merchant = getAccountById(merchant["account_id"])
        transactionItem = intTransactionEntity(merchant['account_id'], transactionCreateRequest)
        print("transactionItem: ", transactionItem)
        return saveTransaction(transactionItem)
    return None


def verify_transaction(auth_token, transaction_id):
    personal = getPersonalAccountByToken(auth_token)
    print("personal: ", personal)
    print("verify the transaction_id: ", transaction_id)
    if personal is not None:
        personalId = personal["account_id"]
        personalContent = getAccountById(personalId)
        transactionContent = getTransactionById(transaction_id)

        net = float(personalContent["balance"]) - float(transactionContent["amount"]) - float(personalContent["credit"])
        if net > 0:
            personalContent["credit"] = float(personalContent["credit"]) + float(transactionContent["amount"])
            updateAccount(personalContent)
            transaction = updateConfirmedStatusByTransactionId(transaction_id, personal["account_id"])
            print("verify transaction: ", transaction)
            return transaction

    return updateFailedStatusByTransactionId(transaction_id, personal["account_id"])


def confirm_transaction(auth_token, transactionConfirmRequest):
    print("confirm transaction")
    return "confirm transaction"


def cancel_transaction(auth_token, transactionConfirmRequest):
    print("cancel transaction")
    return "cancel transaction"


def updateConfirmedStatusByTransactionId(transaction_id, personalId):
    return updateStatusByTransactionId(transaction_id, TransactionType.VERIFIED, personalId)


def updateVerifiedStatusByTransactionId(transaction_id):
    return updateStatusByTransactionId(transaction_id, TransactionType.VERIFIED)


def updateCompletedStatusByTransactionId(transaction_id):
    return updateStatusByTransactionId(transaction_id, TransactionType.COMPLETED)


def updateCanceledStatusByTransactionId(transaction_id):
    return updateStatusByTransactionId(transaction_id, TransactionType.CANCELED)


def updateExpiredStatusByTransactionId(transaction_id):
    return updateStatusByTransactionId(transaction_id, TransactionType.EXPIRED)


def updateFailedStatusByTransactionId(transaction_id, personalId):
    return updateStatusByTransactionId(transaction_id, TransactionType.FAILED, personalId)


def updateStatusByTransactionId(transaction_id, status, personalId = None):
    entity = getTransactionById(transaction_id)
    entity["status"] = status
    if personalId is not None:
        entity["outcome_account"] = personalId
    return updateTransaction(entity)