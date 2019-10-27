import mysql.connector
import socket
import socks
import pickle
login = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="lipton123"
)
host = '127.0.0.1'
port = 1337
socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050, True)
soc = socks.socksocket()
soc.bind((host, port))
soc.listen()
conn, addr = soc.accept()
print(login)
pointer = login.cursor()
with conn:
        print('Connected by: ', addr)
        while True:
            data = conn.recv(4096)
            data_map = pickle.loads(data)
            print(repr(data_map))
            if not data: break

            #conn.send(data)
            #sql = 'INSERT INTO login (username, password) VALUES (%s, %s)'
            #val = (data,)
