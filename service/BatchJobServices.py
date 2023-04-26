import datetime
from apscheduler.schedulers.blocking import BlockingScheduler


def batch_job():
    # put your batch job code here
    print("Batch job running at", datetime.datetime.now())


def start_batch_job():
    # Create a scheduler object
    scheduler = BlockingScheduler()

    # Define the job to run the update_database() function every 24 hours
    scheduler.add_job(batch_job, 'interval', seconds=1)

    # Start the scheduler
    scheduler.start()
