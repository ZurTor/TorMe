from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import load_pem_private_key
import time
import os
if not (os.path.exists('pubkey') or os.path.exists('privatekey')):
    key = rsa.generate_private_key(435274713163, 4096, backend=default_backend())
    with open('prvkey', 'w') as f:
        f.write(key.private_bytes(encoding=serialization.Encoding.PEM,format=serialization.PrivateFormat.TraditionalOpenSSL,encryption_algorithm=serialization.NoEncryption()))
    with open('pubkey', 'wb') as f:
        f.write(key)
