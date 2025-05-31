#!/usr/bin/python3
from fabric.api import env, run, put, sudo, local
from os.path import exists
from time import strftime

env.hosts = ['3.86.189.117', '54.236.227.49']
env.user = 'ubuntu'


def do_pack():
    """Create a .tgz archive from web_static/ folder"""
    try:
        local("mkdir -p versions")
        timestamp = strftime("%Y%m%d%H%M%S")
        archive = f"versions/web_static_{timestamp}.tgz"
        local(f"tar -cvzf {archive} web_static")
        return archive
    except Exception:
        return None


def do_deploy(archive_path):
    """Distribute the archive to web servers"""
    if not exists(archive_path):
        return False

    file_name = archive_path.split("/")[-1]
    folder_name = file_name.split(".")[0]
    release_path = f"/data/web_static/releases/{folder_name}"

    try:
        put(archive_path, "/tmp/")
        sudo(f"mkdir -p {release_path}")
        sudo(f"tar -xzf /tmp/{file_name} -C {release_path}")
        sudo(f"rm /tmp/{file_name}")
        sudo(f"mv {release_path}/web_static/* {release_path}/")
        sudo(f"rm -rf {release_path}/web_static")
        sudo("rm -rf /data/web_static/current")
        sudo(f"ln -s {release_path} /data/web_static/current")
        return True
    except Exception:
        return False


def deploy():
    """Automate full deployment"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
