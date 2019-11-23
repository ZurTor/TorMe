import subprocess
import os
os.system("taskkill /F /im tor.exe")
process = subprocess.Popen("resources/app/Tor/tor.exe")
