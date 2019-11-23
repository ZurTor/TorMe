import Cryptodome
import os.path
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome import Random

def create_key():
    rand = Random.new().read
    key = RSA.generate(4096, rand)
    pub_key = key.publickey()
    cipher = PKCS1_OAEP.new(pub_key)
    cipherpriv = PKCS1_OAEP.new(key)

def server_crypt(message):
    with open("resources/app/server_key", "r") as f:
        key = RSA.import_key(f.read())
    cipher = PKCS1_OAEP.new(key)
    return cipher.encrypt(str(message).encode())

def genkey():
    if not os.path.exists("privkey.key"):
        create_key()
        with open("privkey.key", "wb") as f:
            f.write(key.export_key("PEM"))
    else:
        with open("privkey.key", "r") as f:
            key = RSA.import_key(f.read())
        with open("pubkey.key", "wb") as x:
            x.write(key.publickey().export_key("PEM"))
