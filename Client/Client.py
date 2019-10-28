import requests
import jsonpickle
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import uuid
from random import randint

Session_Id=''


def print_menu():
    print("------------------ Client Secure File Upload/Download App ----------------------\n")
    print("1.Connect\n")
    print("2.Upload\n")
    print("3.Download\n")
    print("4.Exit\n")
    print("---------------------------------------------------------------------------------\n")


def connect():
    response = requests.get("http://localhost:5000/public_key_exchange_api/pke")
    pubkey = RSA.import_key(response.content)
    encryptor = PKCS1_OAEP.new(pubkey)
    Sessiondict = {'SessionKey':uuid.uuid1().hex,'nonce':randint(9180483,999999239992399)}
    print("Before Connection..\n")
    print(Sessiondict)
    nonce = Sessiondict['nonce']
    Session_Id = Sessiondict['SessionKey']
    encrypted = encryptor.encrypt(bytes(str(Sessiondict),'utf-8'))
    PARAMS={'packet':encrypted}
    print("Encrypted Session Key and nonce: \n")
    print(PARAMS)
    response = requests.get("http://localhost:5000/public_key_exchange_api/connect",json={"packet": str(encrypted)})
    print("After connection..\n")
    print(response.content)
    if int(response.content) == (nonce+1):
        return True
    else:
        print("Incorrect Nonce Recieved\n")
        return False

if __name__=='__main__':
    while(True):
        print_menu()
        choice = input("Please enter your choice: ")
        if int(choice) == 1 and connect():
            print("Connected!\n")
        else:
            break







