import crypt
import mysql.connector
from mysql.connector import Error
import socket
import socks
import pickle
import json
import time
import random
import secrets
from Cryptodome.Hash import keccak
from threading import Thread
database = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="7tokyonut++", #6nutgirls
  database="login"
)
cursor = database.cursor()
sqlReg = "INSERT INTO userdata (username, password, pubkey) VALUES (%s, %s, %s)"
host = '127.0.0.1'
port = 1337
socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050, True)
def checkMsg():
    pass
def register(jsonReg, pubkey):
    print("\nUSERNAME: ", jsonReg["username"])
    cursor.execute("SELECT * from userdata WHERE username = %(username)s", {'username': jsonReg["username"]})
    rows = cursor.fetchone()
    if rows == None:
        cursor.execute(sqlReg, (jsonReg["username"], hashSHA(jsonReg["password"]), pubkey["pubkey"]))
        database.commit()
    else:
        print(rows)
def sendKey(jsonLog, conn):
    cursor.execute("SELECT pubkey from userdata WHERE username = %(username)s", {'username': jsonLog["username"]})
    rows = cursor.fetchone()
    conn.sendall(pickle.dumps(rows[0]))
def login(jsonLog, conn):
    cursor.execute("SELECT * from userdata WHERE username = %(username)s", {'username': jsonLog["username"]})
    rows = cursor.fetchone()
    if rows == None:
        print("u don't exist bro")
    #database.commit()
    else:
        if hashSHA(jsonLog["password"]) == rows[1].decode():
            print("pass good")
            token = "token:" + secrets.token_urlsafe(100)
            conn.sendall(pickle.dumps(crypt.encryptToken(rows[2].decode().replace('\\n', '\n')[2:-1:], token)))
            cursor.execute("UPDATE userdata SET token = %s WHERE username = %s", (hashSHA(token), jsonLog["username"]))
            database.commit()
        else:
            print("bad pass :(")
            conn.sendall(pickle.dumps("bad pass bro"))
def addMsg(jsonLog, message):
    cursor.execute("SELECT data from userdata WHERE username = %(username)s", {'username': jsonLog["destUser"]})
    data = cursor.fetchone()
    print(message)
    print("\n\n")
    print(data[0])
    try:
        picklist = pickle.loads(data[0])
        picklist.append(message)
    except:
        picklist = []
        picklist.append(message)
    dataBack = pickle.dumps(picklist)
    print("git prawie")
    print(jsonLog["destUser"])
    try:
        print("nie majonez")
        cursor.execute('''UPDATE userdata SET data = %s WHERE username = %s''', (dataBack, jsonLog["destUser"]))
        print("majonze")
        database.commit()
    except mysql.connector.Error as error:
        print("Eroor")
        print("Failed inserting BLOB data into MySQL table {}".format(error))






def hashSHA(mess):
    keccak_hash = keccak.new(digest_bits=512)
    keccak_hash.update(bytes(mess.encode()))
    return keccak_hash.hexdigest()

def on_new_client(clientsocket,addr):
    try:
        print('Connected by: ', addr)
        data = b''
        while True:
            packet = clientsocket.recv(16)
            print(packet)
            data += packet
            if (packet[-3] == 1 and packet[-2] == 97) or (packet[-3] == 2 and packet[-2] == 101): break
        print("help")
        data_map_list = pickle.loads(data)
        jsonLog = json.loads(crypt.decrypt(data_map_list[0]))
        print(jsonLog)
        if jsonLog["type"] == "login":
            login(jsonLog, clientsocket)
        if jsonLog["type"] == "register":
            pubkey = json.loads(data_map_list[1])
            register(jsonLog, pubkey)
        if jsonLog["type"] == "getKey":
            sendKey(jsonLog, clientsocket)
        if jsonLog["type"] == "sendMsg":
            addMsg(jsonLog, data_map_list[1])
    except:
        pass

soc = socks.socksocket(socket.AF_INET, socket.SOCK_STREAM)
soc.bind((host, port))
soc.listen()
#print(login)
#pointer = login.cursor()
while True:
    conn, addr = soc.accept()

    Thread(target=on_new_client,args=(conn,addr)).start()
