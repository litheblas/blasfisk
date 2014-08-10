# -*- coding: utf-8 -*-
import multiprocessing

command = '/opt/venvs/blasfisk/bin/gunicorn'
pythonpath = '/opt/blasfisk/blasfisk'
bind = '127.0.0.1:8000'
workers = multiprocessing.cpu_count() * 2 + 1
user = None
logfile = '/opt/venvs/blasfisk/log/gunicorn/blasfisk.log'
loglevel = 'debug'
worker_tmp_dir = '/opt/venvs/blasfisk/tmp/'