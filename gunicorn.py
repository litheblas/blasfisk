import multiprocessing

command = '/opt/litheblas.org/bin/gunicorn'
pythonpath = '/opt/litheblas.org/litheblas'
bind = '127.0.0.1:8000'
workers = multiprocessing.cpu_count() * 2 + 1
#user = 'nobody'