#!/usr/bin/python3
"""Fabric script which generates a tgz archive"""

from datetime import datetime
from fabric import Connection 
from os.path import isdir
import subprocess
import os

def do_pack():
    """TGZ"""
    local = Connection('localhost')
    try:
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        if isdir("versions") is False:
            os.mkdir("versions")
        file_name = "versions/web_static_{}.tgz".format(date)
        subprocess.run(["tar", "-cvzf", file_name, "web_static"], check=True)
        print("Test")
        return file_name
    except Exception as e:
        print("Error: %d",e)
        return None

def main():
    do_pack()

if __name__ == "__main__":
    main()          

