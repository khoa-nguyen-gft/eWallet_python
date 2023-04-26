import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

from service.TransactionService import updateExpiredStatusByTransactionId


def batch_job():
    # put your batch job code here
    listTransaction = updateExpiredStatusByTransactionId()
    if listTransaction is not None and len(listTransaction) != 0:
        print(datetime.datetime.now(), " List transaction is expired: ", listTransaction)


def start_batch_job():
    # Create a scheduler object
    scheduler = BlockingScheduler()

    # Define the job to run the update_database() function every 24 hours
    scheduler.add_job(batch_job, 'interval', seconds=6*60)

    # Start the scheduler
    scheduler.start()
