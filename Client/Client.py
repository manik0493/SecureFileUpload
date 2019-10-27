import requests
import jsonpickle
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
response = requests.get("http://localhost:5000/public_key_exchange_api/pke")

pubkey = RSA.import_key(response.content)

encryptor = PKCS1_OAEP.new(pubkey)
encrypted = encryptor.encrypt(b'Hi')
PARAMS={'msg':encrypted}

res2 = requests.get("http://localhost:5000/public_key_exchange_api/message",json={"msg": str(encrypted)})

print(res2.content)




