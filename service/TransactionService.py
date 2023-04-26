
from entities.Transaction import intTransactionEntity
from repository.AccountRepository import get_by_id
from repository.TransactionRepository import save
from service.TokenService import get_merchant_account_by_token


def create_transaction(auth_token, transactionCreateRequest):
    merchant = get_merchant_account_by_token(auth_token)
    print("merchant: ", merchant)
    print("transactionCreateRequest: ", transactionCreateRequest)
    if merchant is not None:
        merchant = get_by_id(merchant["account_id"])
        transactionItem = intTransactionEntity(merchant['account_id'], transactionCreateRequest)
        save(transactionItem)

    print("create transaction")
    return "create transaction"


def confirm_transaction(auth_token, transactionConfirmRequest):
    print("confirm transaction")
    return "confirm transaction"


def verify_transaction(auth_token, transactionConfirmRequest):
    print("verify transaction")
    return "verify transaction"


def cancel_transaction(auth_token, transactionConfirmRequest):
    print("cancel transaction")
    return "cancel transaction"


