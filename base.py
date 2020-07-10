# base.py
#
# Peter Toth
# 6 May 2020

import os
from pathlib import Path
import shutil
import socket

PROGRAM_HOME_DIR = str(Path.home()) + "\\.apassist\\"

def setup_home():
    os.makedirs(PROGRAM_HOME_DIR)
    os.makedirs(PROGRAM_HOME_DIR+"uploads")
    shutil.copytree("base", PROGRAM_HOME_DIR+"base")

def setup_files():
    if not os.path.exists(PROGRAM_HOME_DIR):
            setup_home()
    else:
        reset()

def reset():
    shutil.rmtree(PROGRAM_HOME_DIR)
    setup_home()

def getIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]