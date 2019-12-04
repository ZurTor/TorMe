import connect
import socket
import socks
import pickle
import cipher
import json
import time
from threading import Thread
from Cryptodome.Hash import keccak
import threading
class Unbuffered(object):
   def __init__(self, stream):
       self.stream = stream
   def write(self, data):
       self.stream.write(data)
       self.stream.flush()
   def writelines(self, datas):
       self.stream.writelines(datas)
       self.stream.flush()
   def __getattr__(self, attr):
       return getattr(self.stream, attr)
lock = threading.Lock()
import sys
sys.stdout = Unbuffered(sys.stdout)
def send(soc, picklist):
    print("send")
    soc.sendall(pickle.dumps(picklist))
def recv(soc):
    print("recv")
    data=b''
    while True:
        packet = soc.recv(4096)
        if not packet: break
        data+=packet
    print(pickle.loads(data))
def sleeprecv():
    time.sleep(6)
    with lock:
        Thread(target=recv, args=(soc, )).start()
#tor = connect.run_tor()
host = '127.0.0.1'
port = 1337
socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050, True)
soc = socks.socksocket(socket.AF_INET, socket.SOCK_STREAM)
key_active = False
cipher.genkey()
try:
    soc.connect(("qnvzyabvnrx5twf7rpbbhklmlgvn2rdq3hkvpgnq5rik3gnvalybl6ad.onion", port))
except:
    print("maybe connected :?")
while True:
    args = input().split(' ')
    if args[0] == "login":

        login = {"type":"login", "username": args[1], "password": args[2]}
        #login.insert(0,"login")
        jsonlog = json.dumps(login)
        login_bytes = cipher.server_crypt(jsonlog)
        print(jsonlog)
        picklist = []
        picklist.append(login_bytes)
        print(picklist[0])
        #soc.sendall(pickle.dumps(picklist))
        Thread(target=send, args=(soc, picklist, )).start()
        #Thread(target=sleeprecv).start()
        print("XD")
    if args[0] == "register":

        register = {"type":"register", "username": args[1], "password": args[2]}
        #login.insert(0,"login")
        jsonlog = json.dumps(register)
        reg_bytes = cipher.server_crypt(jsonlog)
        print(jsonlog)
        pubson = json.dumps({"pubkey": str(cipher.return_pub())})
        picklist = []
        picklist.append(reg_bytes)
        picklist.append(pubson)
        try:
            soc.sendall(pickle.dumps(picklist))
        except:
            print("disconnected")

    #try:
    #    data = soc.recv(4096)
    #    data_map = pickle.loads(data)
    #    jsonLog = json.loads(str(crypt.decrypt(data_map).decode()))
    #'{"username":"karbs", "password":"krabs"}'
