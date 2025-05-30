#!/usr/bin/python3
"""Fabric 3 script to generate .tgz archive from web_static folder."""

from fabric import task
from datetime import datetime
import os

@task
def do_pack(c):
    """Create archive from web_static folder."""
    now = datetime.now()
    archive_name = f"versions/web_static_{now.strftime('%Y%m%d%H%M%S')}.tgz"

    if not os.path.exists("versions"):
        os.makedirs("versions")

    result = c.local(f"tar -cvzf {archive_name} web_static")

    if result.ok:
        print(f"web_static packed: {archive_name} -> {os.path.getsize(archive_name)} Bytes")
        return archive_name
    else:
        return None
