import os
import subprocess

def run_tor():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.system("killall tor")
    return subprocess.Popen([dir_path + '/tor'])
