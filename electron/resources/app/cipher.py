import Cryptodome
import os.path
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome import Random
import pickle
def index_finder(data, user):
    for i in range(len(pickle.loads(data))):
        if any(user in s for s in pickle.loads(data)[i].split("::")):
            return i
def create_key():
    rand = Random.new().read
    key = RSA.generate(8196, rand)
    pub_key = key.publickey()
    cipher = PKCS1_OAEP.new(pub_key)
    cipherpriv = PKCS1_OAEP.new(key)
    return key
def hashSHA(mess):
    keccak_hash = keccak.new(digest_bits=512)
    keccak_hash.update(bytes(mess.encode()))
    return keccak_hash.hexdigest()
def server_crypt(message):
    with open("resources/app/server_key", "r") as f:
        key = RSA.import_key(f.read())
    cipher = PKCS1_OAEP.new(key)
    return cipher.encrypt(str(message).encode())
def client_crypt(message, user):
    with open("resources/app/temp/pubkeys", "rb") as f:
        data = f.read()
        key = RSA.import_key(pickle.loads(data)[index_finder(data, user)].split("::")[1])
    cipher = PKCS1_OAEP.new(key)
    return cipher.encrypt(str(message).encode())
def decode_priv(message):
    with open("resources/app/privkey.key", "r") as f:
        key = RSA.import_key(f.read())
    cipher = PKCS1_OAEP.new(key)
    return cipher.decrypt(message)
def return_pub():
    with open("resources/app/privkey.key", "r") as f:
        key = RSA.import_key(f.read())
        return key.publickey().export_key("PEM")
def genkey():
    if not os.path.exists("resources/app/privkey.key"):
        key = create_key()
        with open("resources/app/privkey.key", "wb") as f:
            f.write(key.export_key("PEM"))
        with open("resources/app/pubkey.key", "wb") as x:
            x.write(key.publickey().export_key("PEM"))
    else:
        with open("resources/app/privkey.key", "r") as f:
            key = RSA.import_key(f.read())
        with open("resources/app/pubkey.key", "wb") as x:
            x.write(key.publickey().export_key("PEM"))
