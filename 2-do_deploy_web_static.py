# -*- coding: utf-8 -*-
#!/usr/bin/python3
from fabric.api import env, run, put
import os

# ✅ Correct IPs of your web-01 and web-02 servers
env.hosts = ['3.86.189.117', '54.236.227.49']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'  # Make sure this is your private key path

def do_deploy(archive_path):
    """Distributes an archive to the web servers."""
    if not os.path.exists(archive_path):
        return False
    try:
        file_name = archive_path.split("/")[-1]
        folder_name = "/data/web_static/releases/" + file_name.split(".")[0]

        put(archive_path, "/tmp/")
        run("mkdir -p {}".format(folder_name))
        run("tar -xzf /tmp/{} -C {}".format(file_name, folder_name))
        run("rm /tmp/{}".format(file_name))
        run("mv {}/web_static/* {}".format(folder_name, folder_name))
        run("rm -rf {}/web_static".format(folder_name))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(folder_name))

        # ✅ Create symlink so that /hbnb_static points to the deployed content
        run("sudo ln -sf /data/web_static/current /var/www/html/hbnb_static")

        print("New version deployed!")
        return True
    except Exception as e:
        print("Deployment failed:", e)
        return False
