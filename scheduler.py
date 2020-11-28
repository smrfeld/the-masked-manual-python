from apscheduler.schedulers.blocking import BlockingScheduler
from fetch_helpers import fetch_latest

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=3)
def timed_job():
    print('Fetching latest according to schedule: every 3 minutes')
    fetch_latest(from_cache=False)
 
# Run once a week
@sched.scheduled_job('cron', day_of_week='mon', hour=0)
def scheduled_job():
    print('Fetching latest according to schedule: every monday at 00:00')
    fetch_latest(from_cache=False)

# Run schedule
sched.start()
