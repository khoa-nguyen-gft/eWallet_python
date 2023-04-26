from datetime import datetime, timezone

from entities.Transaction import (
    intTransactionEntity,
    TransactionType
)
from repository.AccountRepository import getAccountById, updateAccount
from repository.TransactionRepository import (
    getTransactionById,
    saveTransaction,
    updateTransaction,
    getTransactionByIdAndListStatus
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
        return {"transaction": saveTransaction(transactionItem), "incomeAccount": merchant, "outcomeAccount": None}
    return None


def confirm_transaction(auth_token, transaction_id):
    personal = getPersonalAccountByToken(auth_token)
    print("personal: ", personal)
    print("confirm the transaction_id: ", transaction_id)
    incomeAccount = None
    account = None

    if personal is not None:
        print("start process confirm")

        personalId = personal["account_id"]
        personalContent = getAccountById(personalId)
        transactionContent = getTransactionById(transaction_id)
        account = getAccountById(personalId)
        incomeAccount = getAccountById(transactionContent["income_account"])
        transactionStatus = transactionContent["status"]

        if transactionStatus == TransactionType.CONFIRMED:
            print("This transaction is confirmed....")
            return {"transaction": transactionContent, "incomeAccount": incomeAccount, "outcomeAccount": account}

        # verify the person have enough the money to pay
        net = float(personalContent["balance"]) - float(transactionContent["amount"])
        if net > 0 and transactionStatus == TransactionType.INITIALIZED:
            transaction = updateConfirmedStatusByTransactionId(transaction_id, personalId)
            print("verify transaction: ", transaction)
            return {"transaction": transaction, "incomeAccount": incomeAccount, "outcomeAccount": account}

    return {"transaction": updateFailedStatusByTransactionId(transaction_id, personal["account_id"]),
            "incomeAccount": incomeAccount,
            "outcomeAccount": account
            }


def verify_transaction(auth_token, transaction_id):
    personal = getPersonalAccountByToken(auth_token)

    print("personal: ", personal)
    print("verify the transaction_id: ", transaction_id)
    merchantContent = None
    personalContent = None
    personalId = None

    if personal is not None:
        personalId = personal["account_id"]
        personalContent = getAccountById(personalId)
        transactionContent = getTransactionById(transaction_id)
        transactionStatus = transactionContent["status"]
        merchantContent = getAccountById(transactionContent["income_account"])

        if transactionStatus == TransactionType.VERIFIED or transactionStatus == TransactionType.COMPLETED:
            print("This transaction is verified....")
            return {"transaction": transactionContent, "incomeAccount": merchantContent, "outcomeAccount": personalContent}

        net = float(personalContent["balance"]) - float(transactionContent["amount"])
        if net > 0 and transactionStatus == TransactionType.CONFIRMED:
            personalContent["balance"] = float(personalContent["balance"]) - float(transactionContent["amount"])
            print("personalContent", personalContent)
            updateAccount(personalContent)

            merchantContent["balance"] = merchantContent["balance"] + float(transactionContent["amount"])
            print("merchantContent", merchantContent)
            updateAccount(merchantContent)
            transaction = updateCompletedStatusByTransactionId(transaction_id, personalId)
            print("verify transaction: ", transaction)
            return {"transaction": transaction, "incomeAccount": merchantContent, "outcomeAccount": personalContent}

    return {"transaction": updateFailedStatusByTransactionId(transaction_id, personalId),
            "incomeAccount": merchantContent,
            "outcomeAccount": personalContent
            }


def cancel_transaction(auth_token, transaction_id):
    personal = getPersonalAccountByToken(auth_token)
    print("personal: ", personal)
    print("confirm the transaction_id: ", transaction_id)

    if personal is not None:
        personalId = personal["account_id"]
        transactionContent = getTransactionById(transaction_id)
        account = getAccountById(personalId)
        incomeAccount = getAccountById(transactionContent["income_account"])
        transactionStatus = transactionContent["status"]

        if transactionStatus == TransactionType.CANCELED:
            print("This transaction is Canceled....")
            return {"transaction": transactionContent, "incomeAccount": incomeAccount, "outcomeAccount": account}

        if transactionStatus == TransactionType.CONFIRMED:
            transaction = updateCanceledStatusByTransactionId(transaction_id, personalId)
            print("cancel transaction: ", transaction)
            return {"transaction": transaction, "incomeAccount": incomeAccount, "outcomeAccount": account}

    return {"transaction": updateFailedStatusByTransactionId(transaction_id, personal["account_id"]),
            "incomeAccount": incomeAccount,
            "outcomeAccount": account
            }


def updateConfirmedStatusByTransactionId(transaction_id, personalId):
    return updateStatusByTransactionId(transaction_id, TransactionType.CONFIRMED, personalId)


def updateVerifiedStatusByTransactionId(transaction_id, personalId):
    return updateStatusByTransactionId(transaction_id, TransactionType.VERIFIED, personalId)


def updateCompletedStatusByTransactionId(transaction_id, personalId):
    return updateStatusByTransactionId(transaction_id, TransactionType.COMPLETED, personalId)


def updateCanceledStatusByTransactionId(transaction_id, personalId):
    return updateStatusByTransactionId(transaction_id, TransactionType.CANCELED, personalId)


def updateExpiredStatusByTransactionId():
    listTransaction = getTransactionByIdAndListStatus([TransactionType.INITIALIZED, TransactionType.CONFIRMED, TransactionType.VERIFIED])
    for transaction in listTransaction:
        updateTimeTransaction = datetime.strptime( transaction["update_date"], '%Y-%m-%d %H:%M:%S.%f').timestamp()
        now = datetime.now(timezone.utc).timestamp()

        if now - updateTimeTransaction >= 5:
            transaction["status"] = TransactionType.EXPIRED
            updateTransaction(transaction)
    return listTransaction


def updateFailedStatusByTransactionId(transaction_id, personalId):
    return updateStatusByTransactionId(transaction_id, TransactionType.FAILED, personalId)


def updateStatusByTransactionId(transaction_id, status, personalId=None):
    entity = getTransactionById(transaction_id)
    entity["status"] = status
    if personalId is not None:
        entity["outcome_account"] = personalId
    return updateTransaction(entity)
