import sys
import os
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')+r"\app")
if not path in sys.path:
    sys.path.insert(1, path)
del path
import socket
import socks
import pickle
import cipher
import json
import time
from datetime import datetime
from threading import Thread
from Cryptodome.Hash import keccak
import threading
import random

class Error(Exception):
    def __init__(self, message):
        self.message = message

def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except:
        return False
    return True


args = input()
if not is_json(args):
    args = args.split(' ')

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

    try:
        soc.connect(("qnvzyabvnrx5twf7rpbbhklmlgvn2rdq3hkvpgnq5rik3gnvalybl6ad.onion", port))
    except:
        raise Error("Server offline!")

    #soc.sendall(pickle.dumps({"type":"connid", "id":hashSHA(args[0]+"nuggets")}))


    if args[0] == "login":
        login = {"type":"login", "username": args[1], "password": args[2]}
        #login.insert(0,"login")
        with open("resources/app/temp/user", "w") as f:
            f.write(args[1])
        jsonlog = json.dumps(login)
        login_bytes = cipher.server_crypt(jsonlog)
        pubson = json.dumps({"pubkey": str(cipher.return_pub())})
        picklist = []
        picklist.append(login_bytes)
        picklist.append(pubson)
        soc.sendall(pickle.dumps(picklist) + b'XDD')
        data = b''
        while True:
            packet = soc.recv(16)
            data += packet
            if packet[-2] == 0 and packet[-1] == 46: break
        try:
            if cipher.decode_priv(pickle.loads(data)).decode().split(':')[0] == "token":
                with open("resources/app/temp/token", "w") as f:
                    f.write(cipher.decode_priv(pickle.loads(data)).decode())
                print("token")
        except:
            print(pickle.loads(data))
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
        soc.sendall(pickle.dumps(picklist) + b'XDD')
        data = b''
        while True:
            packet = soc.recv(16)
            print(packet)
            data += packet
            if packet[-2] == 0 and packet[-1] == 46: break
        print(pickle.loads(data))
    if is_json(args):
        print(json.loads(args))
        if json.loads(args)["0"] == "sendMsg":
            f = open("resources/app/temp/token", "r")
            token = f.read()
            curruser = open("resources/app/temp/curruser", "r").read()
            user = open("resources/app/temp/user", "r").read()
            now = datetime.now()
            sendMsg = {"type" : "sendMsg", "destUser" : curruser, "token" : token, "mainUser" : user, "time" : json.loads(args)["2"]}
            jsonlog = json.dumps(sendMsg)
            msg_bytes = cipher.server_crypt(jsonlog)
            picklist = []
            picklist.append(msg_bytes)
            print(curruser)
            picklist.append(cipher.client_crypt(json.loads(args)["1"], curruser))
            soc.sendall(pickle.dumps(picklist) + b'XDD')
    if args[0] == "getMsg":
        f = open("resources/app/temp/token", "r")
        token = f.read()
        user = open("resources/app/temp/user", "r").read()
        sendMsg = {"type" : "getMsg", "token" : token, "username" : user}
        jsonlog = json.dumps(sendMsg)
        msg_bytes = cipher.server_crypt(jsonlog)
        picklist = []
        picklist.append(msg_bytes)
        soc.sendall(pickle.dumps(picklist) + b'XDD')
        data = b''
        while True:
            packet = soc.recv(16)
            data += packet
            if (data[-3] == 88 and data[-2] == 68 and data[-1] == 68): break
        data = data[:-3:]
        if data != b'':
            try:
                backlist = pickle.loads(data)
            except:
                raise Error("Unstable connection!")
            inString = ""
            print(backlist)
            for i in range(0, len(backlist), 3):
                back_time = backlist[i]
                who = backlist[i+1]
                inString = cipher.decode_priv(backlist[i+2]).decode()
                print(json.dumps({"msg":inString, "user":who, "time":back_time}, ensure_ascii=False))
        soc.close()
    if args[0] == "getPubkey":
        data = b''
        f = open("resources/app/temp/pubkeys", "rb+")
        datafile = f.read() + pickle.dumps(' ')
        f.close()
        fw = open("resources/app/temp/pubkeys", "wb")
        print(args[1])
        if not any(args[1] in s for s in pickle.loads(datafile)):
            datafile = datafile[:-1:]
            getKey = {"type" : "getKey", "username" : args[1]}
            jsonlog = json.dumps(getKey)
            key_bytes = cipher.server_crypt(jsonlog)
            picklist = []
            picklist.append(key_bytes)
            soc.sendall(pickle.dumps(picklist) + b'XDD')
            while True:
                packet = soc.recv(16)
                print(packet)
                data += packet
                try:
                    if packet[-2] == 0 and packet[-1] == 46: break
                except:
                    raise Error("Unstable connection!")
            try:
                publist = pickle.loads(datafile)
                publist.append(args[1] + "::" + pickle.loads(data).decode().replace('\\n', '\n')[2:-1:])
            except:
                publist = []
                publist.append(args[1] + "::" + pickle.loads(data).decode().replace('\\n', '\n')[2:-1:])
            fw.write(pickle.dumps(publist))
            fw.close()
        else:
            fw.write(datafile[:-1:])
            soc.sendall(cipher.server_crypt(pickle.dumps("nice")+b'XDD'))
            soc.close()
        with open("resources/app/temp/curruser", "w") as f:
            f.write(args[1])
    #try:
    #    data = soc.recv(4096)
    #    data_map = pickle.loads(data)
    #    jsonLog = json.loads(str(crypt.decrypt(data_map).decode()))
    #'{"username":"karbs", "password":"krabs"}'
