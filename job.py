from apscheduler.schedulers.blocking import BlockingScheduler
from main import poll_transactions

scheduler = BlockingScheduler()
scheduler.add_job(poll_transactions, 'interval', seconds=30)
scheduler.start()
