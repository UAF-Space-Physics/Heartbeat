#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 13:35:34 2016

@author: john
"""

file_name   = 'log_stats.txt'
remote_path = '/home/$USER/Camera_status'
hostname    = '$USER@website.alaska.edu'

import logging

logger    = logging.getLogger('Heartbeat')
fh        = logging.FileHandler('Heartbeat.log')
ch        = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)

logger.setLevel  (logging.DEBUG)
fh.setLevel      (logging.DEBUG)
ch.setLevel      (logging.DEBUG)


import socket
#Open a socket and try to connect to test_site using test_port.
#Record the entrypoint for this connection (our IP) and return
def get_ip_addr(test_site='8.8.8.8',test_port=80):
    sock = socket.socket   (socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect           (       (test_site,test_port)     )
    ip   = sock.getsockname(                                 )[0]
    sock.close()
    return ip


import psutil as ps
#Get a list of running process IDs and look for ours. Return its
#status once we find it.
def get_status(tag = 'spyder'):
    pids_running = ps.pids()
    status       = 'Offline'
    for pid in pids_running:
        process  = ps.Process  (pid)
        pid_name = process.name(   )
        if tag in pid_name:
            status = process.status()
            break
    return status



import platform as pl
import subprocess

def remote_copy(file_path,hostname,remote_path,passwd=''):
    os = pl.system()

    if 'Windows' in os:
        command = 'scp'
    if 'Linux'   in os:
        #Change this later to be more pythonic
        command = 'scp'

    return subprocess.call(\
                            ['sshpass','-p',passwd,command,file_path,
                            ':'.join([hostname,remote_path])
                            ]
                            )

import time
def create_status_report(file_path='report.txt',process='VirtualBox'):
    time_format  = '%y%m%d-%H%M%S'
    current_time = time.strftime(time_format,time.gmtime())

    hostname= socket.gethostname()
    ip_addr = get_ip_addr()
    status  = get_status (process)
    info    = [current_time,hostname,ip_addr,status]

    try    : message = "\n".join(info)
    except : print(info)

    status_file = open(file_path,'w+')
    status_file.write(message)
    status_file.close()

def start_child():
    logger.debug("Creating Report")
    create_status_report(file_name)
    logger.debug("Done")

    logger.debug("Starting remote copy")
    logger.debug("Process returned:{}".format(remote_copy(file_name,hostname,remote_path)))
    logger.debug("Done")


if __name__== '__main__':
    start_child()
    quit(0)
