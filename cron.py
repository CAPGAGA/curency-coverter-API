from crontab import CronTab
from database import seed_db

cron = CronTab(user=True)

job = cron.new(command="python database.py seed_db")
job.hour.on(0)