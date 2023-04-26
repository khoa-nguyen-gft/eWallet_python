import os
import uuid
from datetime import datetime


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
    # get the creation time of the repository
    now = datetime.now()

    return {
        "transaction_id": str(uuid.uuid4()),
        "merchant_id": merchantId,
        "income_account": merchantId,
        "outcome_account": None,
        "amount": request["amount"],
        "extra_data": request["extraData"],
        "signature": request["signature"],
        "status": TransactionType.INITIALIZED,
        "created_date": str(now),
        "update_date": str(now)
    }