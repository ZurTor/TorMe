import connect
import socket
import socks
import pickle
import cipher
from Cryptodome.Hash import keccak
#tor = connect.run_tor()

host = '127.0.0.1'
port = 1337
socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050, True)
soc = socks.socksocket()
key_active = False

while True:
    try:
        soc.connect(("qnvzyabvnrx5twf7rpbbhklmlgvn2rdq3hkvpgnq5rik3gnvalybl6ad.onion", port))
    except:
        print("maybe works")
    login = list(map(str, input().split(' ')))
    keccak_hash = keccak.new(digest_bits=512)
    keccak_hash.update(login[1])
    login[1] = keccak_hash.hexdigest()
    login_bytes = pickle.dumps(cipher.server_crypt(login))
    soc.sendall(login_bytes)
    #data = soc.recv(4096)
