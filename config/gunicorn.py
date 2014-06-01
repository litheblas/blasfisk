import multiprocessing

command = '/opt/litheblas.org/bin/gunicorn'
pythonpath = '/opt/litheblas.org/litheblas'
bind = '0.0.0.0:8000'
workers = multiprocessing.cpu_count() * 2 + 1
user = None
logfile = '/opt/litheblas.org/log/gunicorn/gunicorn.log'
loglevel = 'info'
worker_tmp_dir = '/opt/litheblas.org/tmp/'