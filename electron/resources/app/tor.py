import subprocess
import os
import sys
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')+r"\app")
if not path in sys.path:
    sys.path.insert(1, path)
del path
os.system("taskkill /F /im tor.exe")
process = subprocess.Popen("resources/app/Tor/tor.exe")
