#!/usr/bin/python
from fabric.api import env, run, put, sudo, local
from os.path import exists
from datetime import datetime

env.hosts = ['3.86.189.117', '54.236.227.49']
env.user = 'ubuntu'


def do_pack():
    """Create a .tgz archive from web_static/ folder"""
    try:
        local("mkdir -p versions")
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        archive = "versions/web_static_{}.tgz".format(timestamp)
        local("tar -cvzf {} web_static".format(archive))
        return archive
    except:
        return None


def do_deploy(archive_path):
    """Distribute the archive to web servers"""
    if not exists(archive_path):
        return False

    file_name = archive_path.split("/")[-1]
    folder_name = file_name.split(".")[0]
    release_path = "/data/web_static/releases/{}".format(folder_name)

    try:
        put(archive_path, "/tmp/")
        sudo("mkdir -p {}".format(release_path))
        sudo("tar -xzf /tmp/{} -C {}".format(file_name, release_path))
        sudo("rm /tmp/{}".format(file_name))
        sudo("mv {}/web_static/* {}".format(release_path, release_path))
        sudo("rm -rf {}/web_static".format(release_path))
        sudo("rm -rf /data/web_static/current")
        sudo("ln -s {} /data/web_static/current".format(release_path))
        return True
    except:
        return False


def deploy():
    """Automate full deployment"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
