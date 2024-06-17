#!/usr/bin/python3
"""Fabric script that distributes an archive to your web servers"""
from fabric import Connection, task
from os.path import exists

# List of hosts to deploy to
hosts = ['3.94.158.116']
user = "ubuntu"
key_filename = "~/.ssh/id_rsa"

@task
def do_deploy(c, archive_path):
    """Function to distribute an archive to your web servers"""
    if not exists(archive_path):
        print("failed")
        return False
    try:
        file_name = archive_path.split("/")[-1]
        name = file_name.split(".")[0]
        path_name = "/data/web_static/releases/" + name

        c.put(archive_path, "/tmp/")
        c.run("mkdir -p {}/".format(path_name))
        c.run('tar -xzf /tmp/{} -C {}/'.format(file_name, path_name))
        c.run("rm /tmp/{}".format(file_name))
        c.run("mv {}/web_static/* {}".format(path_name, path_name))
        c.run("rm -rf {}/web_static".format(path_name))
        c.run('rm -rf /data/web_static/current')
        c.run('ln -s {}/ /data/web_static/current'.format(path_name))
        print("Passed")
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

for host in hosts:
    conn = Connection(host=host, user=user, connect_kwargs={"key_filename": key_filename})
    do_deploy(conn, "/home/keny/Documents/ALU/alu-AirBnB_clone_v2/versions/web_static_20240610003713.tgz")
