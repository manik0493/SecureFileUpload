import requests
import jsonpickle
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import uuid
from random import randint
response = requests.get("http://localhost:5000/public_key_exchange_api/pke")

pubkey = RSA.import_key(response.content)

encryptor = PKCS1_OAEP.new(pubkey)
Sessiondict = {'SessionKey':uuid.uuid1().hex,'nonce':randint(9180483,999999239992399)}
print("Before Connection..\n")
print(Sessiondict)

encrypted = encryptor.encrypt(bytes(str(Sessiondict),'utf-8'))
PARAMS={'packet':encrypted}

response = requests.get("http://localhost:5000/public_key_exchange_api/connect",json={"packet": str(encrypted)})
print("After connection")
print(response.content)

response = requests.get("http://localhost:5000/public_key_exchange_api/sessionbook")

print(response.content)




