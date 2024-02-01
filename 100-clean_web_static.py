#!/usr/bin/python3
"""
Deletes out-of-date archives, using the function do_clean
"""
import os
from datetime import datetime
from fabric.api import *

env.user = "ubuntu"
env.hosts = ["54.144.46.157", "54.167.85.19"]


def do_pack():
    """Compress files from web_static directory"""
    try:
        if not os.path.isdir("versions"):
            os.makedirs("versions")
        date = datetime.now()
        file = "versions/web_static_{0}{1}{2}{3}{4}{5}".format(
            date.year,
            date.month,
            date.day,
            date.hour,
            date.minute,
            date.second
        )
        file += ".tgz"
        local("tar -cvzf {} web_static".format(file))
        return file
    except Exception:
        return None


def do_deploy(archive_path):
    """
    Deploy archive

    Args:
        - archive_path(str, optional): Path of the archive
    """
    try:
        if not os.path.isfile(archive_path):
            return False
        path = archive_path.split("/")[1]
        name = path.split(".")[0]
        put(archive_path, "/tmp/{0}".format(path))
        run("sudo mkdir -p /data/web_static/releases/{}/".format(name))
        source = "sudo tar -xzf /tmp/{0} -C".format(path)
        dest = "/data/web_static/releases/{0}/".format(name)
        run(source + " " + dest)
        run("sudo rm /tmp/{0}".format(path))
        source = (
            "sudo mv /data/web_static/releases/{0}/web_static/*".format(name)
        )
        dest = "/data/web_static/releases/{0}/".format(name)
        run(source + " " + dest)
        run(
            "sudo rm -rf /data/web_static/releases/{0}/web_static".format(name)
        )
        run("sudo rm -rf /data/web_static/current")
        source = "sudo ln -s /data/web_static/releases/{0}/".format(name)
        dest = "/data/web_static/current"
        run(source + " " + dest)
        return True
    except Exception:
        return False


def deploy():
    """
    Full deployment based on do_pack & do_deploy (task 2)
    """
    path = do_pack()
    if path is None:
        return False
    return do_deploy(path)


def do_clean(number=0):
    """
    Delete out-of-date archives
    """
    try:
        if number == 0:
            number = 1
        with cd("versions"):
            local("ls -t | awk 'NR>{}' | xargs sudo rm -f".format(number))
        with cd("/data/web_static/releases"):
            run("ls -t | awk 'NR>{}' | xargs sudo rm -f".format(number))
    except Exception as e:
        print(e)
