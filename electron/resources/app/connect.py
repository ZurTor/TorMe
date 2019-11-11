import connect
import socket
import socks
import pickle
#tor = connect.run_tor()

host = '127.0.0.1'
port = 1337
socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050, True)
soc = socks.socksocket()

while True:
    try:
        soc.connect(("qnvzyabvnrx5twf7rpbbhklmlgvn2rdq3hkvpgnq5rik3gnvalybl6ad.onion", port))
    except:
        print("maybe works")
    login = list(map(str, input().split(' ')))
    login_bytes = pickle.dumps(login)
    soc.sendall(login_bytes)
