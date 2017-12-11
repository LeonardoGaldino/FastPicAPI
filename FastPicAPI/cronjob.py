from crontab import CronTab
import os

path = os.path.dirname(os.path.abspath(__file__))
prev_path = os.path.dirname(path)
file_name = 'manage.py'
command_name = 'changePictureTarget'
full_path = os.path.join(path, file_name)
log_file_name1 = 'logFileSource'
log_file_err1 = 'logFileErrSource'
log_file_name2 = 'logFilePython'
log_file_err2 = 'logfileErrPython'
out1 = '> ' + os.path.join(path, log_file_name1) + ' 2> ' + os.path.join(path, log_file_err1)
out2 = '> ' + os.path.join(path, log_file_name2) + ' 2> ' + os.path.join(path, log_file_err2)
activate_venv = 'source ' + prev_path + '/venv/bin/activate ' + out1
command = 'python ' + full_path + ' ' + command_name + ' ' + out2

# user parameter should be your PC's user!
cron = CronTab(user='lcgm')
cron.env['SHELL'] = '/bin/bash'
cron.env['PATH'] = '/home/lcgm/workspace/Repositories/FastPic/venv/bin:/home/lcgm/bin:/home/lcgm/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin'

job = cron.new(command=activate_venv + ' && '+command)

job.minute.every(1)

cron.write()
