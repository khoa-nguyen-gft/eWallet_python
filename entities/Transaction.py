import uuid


class TransactionType:
    INITIALIZED = 'initialized'
    CONFIRMED = 'confirmed'
    VERIFIED = 'verified'
    COMPLETED = 'completed'
    CANCELED = 'canceled'
    EXPIRED = 'expired'
    FAILED = 'failed'


def intTransactionEntity(merchantId, request) -> dict:
    print("init request: ", request)
    return {
        "transaction_id": str(uuid.uuid4()),
        "merchant_id": merchantId,
        "income_account": merchantId,
        "outcome_account": None,
        "amount": request["amount"],
        "extra_data": request["extraData"],
        "signature": request["signature"],
        "status": TransactionType.INITIALIZED
    }