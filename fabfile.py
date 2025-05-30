from fabric import task
from datetime import datetime
from os.path import exists
import os

# Adjust this to the remote directory where the code should be deployed
remote_dir = "/data/web_static/releases"
current_symlink = "/data/web_static/current"

@task
def do_pack(c):
    """Generate a .tgz archive from the contents of the web_static folder."""
    if not os.path.exists("versions"):
        os.makedirs("versions")
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_path = f"versions/web_static_{timestamp}.tgz"
    print(f"📦 Packing web_static to {archive_path}...")
    result = c.local(f"tar -cvzf {archive_path} web_static", hide=False)
    if result.ok:
        print(f"✅ Archive created: {archive_path}")
        return archive_path
    else:
        print("❌ Failed to create archive")
        return None

@task
def do_deploy(c, archive_path):
    """Distribute the archive to the web servers."""
    if not exists(archive_path):
        print("❌ Archive does not exist")
        return False

    filename = os.path.basename(archive_path)
    folder_name = filename.replace(".tgz", "")
    remote_path = f"{remote_dir}/{folder_name}"

    print(f"🚀 Deploying {filename} to {c.host}...")

    try:
        c.put(archive_path, f"/tmp/{filename}")
        c.run(f"mkdir -p {remote_path}")
        c.run(f"tar -xzf /tmp/{filename} -C {remote_path}")
        c.run(f"rm /tmp/{filename}")
        c.run(f"mv {remote_path}/web_static/* {remote_path}/")
        c.run(f"rm -rf {remote_path}/web_static")
        c.run(f"rm -rf {current_symlink}")
        c.run(f"ln -s {remote_path} {current_symlink}")
        print(f"✅ Successfully deployed on {c.host}")
        return True
    except Exception as e:
        print(f"❌ Deployment failed on {c.host}: {e}")
        return False

@task
def deploy(c):
    """Create and distribute archive to web servers."""
    print("📦 Starting full deployment...")
    archive_path = do_pack(c)
    if not archive_path:
        print("❌ Packaging failed")
        return False
    result = do_deploy(c, archive_path)
    print("✅ Deployment finished!" if result else "❌ Deployment failed")
    return result
