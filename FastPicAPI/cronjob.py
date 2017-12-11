from crontab import CronTab
import os

path = os.path.dirname(os.path.abspath(__file__))
file_name = 'manage.py'
command_name = 'changePictureTarget'
full_path = os.path.join(path, file_name)
log_file_name = 'logfile'
out = '> ' + os.path.join(path, log_file_name) + ' 2> ' + os.path.join(path, log_file_name)
command = 'python ' + full_path + ' ' + command_name + ' ' + out

# user parameter should be your PC's user!
cron = CronTab(user='lcgm')

job = cron.new(command=command)

job.minute.every(1)

cron.write()
