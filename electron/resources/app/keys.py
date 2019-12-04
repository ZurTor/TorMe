import Cryptodome
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP

private_key = RSA.import_key(open("privkey").read())

cipher = PKCS1_OAEP.new(private_key)

def decrypt(message):
    global cipher
    return cipher.decrypt(message)
