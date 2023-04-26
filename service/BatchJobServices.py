import time
import datetime


def batch_job():
    # put your batch job code here
    print("Batch job running at", datetime.datetime.now())


def start_batch_job():
    # run the batch job
    print("Start batch job..........")
    batch_job()

    # wait for 5 minutes before running the batch job again
    time.sleep(60)