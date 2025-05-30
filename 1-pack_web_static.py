#!/usr/bin/python2
# -*- coding: utf-8 -*-

from fabric.api import local
from datetime import datetime

def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.
    Returns the archive path if successful, None otherwise.
    """
    try:
        now = datetime.now()
        archive_name = "versions/web_static_{}{}{}{}{}{}.tgz".format(
            now.year, now.month, now.day, now.hour, now.minute, now.second)
        local("mkdir -p versions")
        local("tar -cvzf {} web_static".format(archive_name))
        return archive_name
    except:
        return None

if __name__ == "__main__":
    do_pack()
