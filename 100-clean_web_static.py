#!/usr/bin/python3
"""
Deletes out-of-date archives, using the function do_clean
"""
from fabric.api import *

env.user = "ubuntu"
env.hosts = ["54.144.46.157", "54.167.85.19"]


def do_clean(number=0):
    """
    Delete out-of-date archives
    """
    number = int(number)
    if number == 0:
        number = 2
    else:
        number += 1
    local('cd versions ; ls -t | tail -n +{} | xargs rm -rf'.format(number))
    path = '/data/web_static/releases'
    run('cd {} ; ls -t | tail -n +{} | xargs rm -rf'.format(path, number))
