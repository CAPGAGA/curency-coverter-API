from crontab import CronTab


cron = CronTab(user=True)

job = cron.new(command="python database.py seed_db")
job.hour.on(0)

cron.write()