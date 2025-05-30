#!/usr/bin/python3
"""distrutes the archive"""
import os.path
from fabric.api import env
from fabric.api import put
from fabric.api import run

env.hosts = ["54.175.253.142", "34.239.255.28"]


def do_deploy(archive_path):
    """gives the archives
    """
    if os.path.isfile(archive_path) is False:
        return False
    fi = archive_path.split("/")[-1]
    nme = fi.split(".")[0]

    if put(archive_path, "/tmp/{}".format(fi)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/".
           format(nme)).failed is True:
        return False
    if run("mkdir -p /data/web_static/releases/{}/".
           format(nme)).failed is True:
        return False
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
           format(fi, nme)).failed is True:
        return False
    if run("rm /tmp/{}".format(fi)).failed is True:
        return False
    if run("mv /data/web_static/releases/{}/web_static/* "
           "/data/web_static/releases/{}/".format(nme, nme)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/web_static".
           format(nme)).failed is True:
        return False
    if run("rm -rf /data/web_static/current").failed is True:
        return False
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".
           format(nme)).failed is True:
        return False
    return True
