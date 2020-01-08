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
import sys
import random

args = input().split(' ')
if not args[0]:
    pass
else:
    #tor = connect.run_tor()
    host = '127.0.0.1'
    port = 1337
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050, True)
    soc = socks.socksocket(socket.AF_INET, socket.SOCK_STREAM)

    key_active = False
    cipher.genkey()

    print("przed conn")
    soc.connect(("qnvzyabvnrx5twf7rpbbhklmlgvn2rdq3hkvpgnq5rik3gnvalybl6ad.onion", port))

    def ret_func():
        return True
    #soc.sendall(pickle.dumps({"type":"connid", "id":hashSHA(args[0]+"nuggets")}))

    print("if")
    if args[0] == "login":
        login = {"type":"login", "username": args[1], "password": args[2]}
        #login.insert(0,"login")
        jsonlog = json.dumps(login)
        login_bytes = cipher.server_crypt(jsonlog)
        picklist = []
        picklist.append(login_bytes)
        soc.sendall(pickle.dumps(picklist) + b'XDD')
        data = b''
        while True:
            packet = soc.recv(16)
            print(packet)
            data += packet
            if packet[-2] == 0 and packet[-1] == 46: break
        if cipher.decode_priv(pickle.loads(data)).decode().split(':')[0] == "token":
            print("token")
            with open("resources/app/temp/token", "w") as f:
                f.write(cipher.decode_priv(pickle.loads(data)).decode())
    if args[0] == "register":
        register = {"type" : "register", "username" : args[1], "password" : args[2]}
        #login.insert(0,"login")
        jsonlog = json.dumps(register)
        reg_bytes = cipher.server_crypt(jsonlog)
        print(jsonlog)
        pubson = json.dumps({"pubkey": str(cipher.return_pub())})
        picklist = []
        picklist.append(reg_bytes)
        picklist.append(pubson)
        soc.sendall(pickle.dumps(picklist))
    if args[0] == "sendMsg":
        f = open("resources/app/temp/token", "r")
        token = f.read()
        curruser = open("resources/app/temp/curruser", "r").read()
        print(curruser)
        sendMsg = {"type" : "sendMsg", "destUser" : curruser, "token" : token}
        print(sendMsg)
        jsonlog = json.dumps(sendMsg)
        msg_bytes = cipher.server_crypt(jsonlog)
        picklist = []
        picklist.append(msg_bytes)
        picklist.append(cipher.client_crypt(args[1]))
        print(picklist[1])
        soc.sendall(pickle.dumps(picklist))
    if args[0] == "getMsg":
        f = open("resources/app/temp/token", "r")
        token = f.read()
        sendMsg = {"type" : "getMsg", "token" : token}
        jsonlog = json.dumps(sendMsg)
        msg_bytes = cipher.server_crypt(jsonlog)
        picklist = []
        picklist.append(msg_bytes)
        soc.sendall(pickle.dumps(picklist))
        data = b''
        while True:
            packet = soc.recv(16)
            print(packet)
            data += packet
            if packet[-2] == 0 and packet[-1] == 46: break
        backlist = pickle.loads(data)
        inString = ""
        for i in range(len(backlist)):
            inString += cipher.decode_priv(backlist[i])
            inString += "\n"
        print(inString)
    if args[0] == "getPubkey":
        getKey = {"type" : "getKey", "username" : args[1]}
        jsonlog = json.dumps(getKey)
        key_bytes = cipher.server_crypt(jsonlog)
        picklist = []
        picklist.append(key_bytes)
        soc.sendall(pickle.dumps(picklist))
        data = b''
        while True:
            packet = soc.recv(16)
            print(packet)
            data += packet
            if packet[-2] == 0 and packet[-1] == 46: break
        with open("resources/app/temp/pubkeys", "w") as f:
            f.write(pickle.loads(data).decode().replace('\\n', '\n')[2:-1:])
        with open("resources/app/temp/curruser", "w") as f:
            f.write(args[1])
    #try:
    #    data = soc.recv(4096)
    #    data_map = pickle.loads(data)
    #    jsonLog = json.loads(str(crypt.decrypt(data_map).decode()))
    #'{"username":"karbs", "password":"krabs"}'
