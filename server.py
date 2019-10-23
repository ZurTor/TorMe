import socket
import socks
host = '127.0.0.1'
port = 80
socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050, True)
with socks.socksocket() as soc:
    soc.bind((host, port))
    soc.listen()
    conn, addr = soc.accept()
    with conn:
            print('Connected by: ', addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                conn.sendall(data)
