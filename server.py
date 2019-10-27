import mysql.connector
import socket
import socks
import pickle
from threading import Thread
login = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="lipton123"
)
host = '127.0.0.1'
port = 1337
socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050, True)

def on_new_client(clientsocket,addr):
    print('Connected by: ', addr)
    while True:
        data = conn.recv(4096)
        if not data: break
        data_map = pickle.loads(data)
        print(repr(data_map))
        clientsocket.send(b"Delivered")
    clientsocket.close()



soc = socks.socksocket()
soc.bind((host, port))
soc.listen()
#print(login)
#pointer = login.cursor()
while True:
    conn, addr = soc.accept()
    Thread(target=on_new_client,args=(conn,addr)).
