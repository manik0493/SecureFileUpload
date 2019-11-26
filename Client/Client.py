from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import uuid, time
from random import randint

from socket_client import JSONClient
import sys, os
sys.path.append('../shared')
from message_type import MessageType


def print_menu():
    print("------------------ Client Secure File Upload/Download App ----------------------\n")
    print("1.Connect\n")
    print("2.Upload\n")
    print("3.Download\n")
    print("4.Exit\n")
    print("---------------------------------------------------------------------------------\n")

class AuthClient(JSONClient):
    def __init__(self, address='localhost', port=10000):
        self.session_id=''
        super().__init__(address, port)

    def auth(self):
        self.send("", msg_type=MessageType.AUTH_REQ)
        response = self.recv()['data'] #requests.get("http://localhost:5000/public_key_exchange_api/pke")
        pubkey = RSA.import_key(response)
        encryptor = PKCS1_OAEP.new(pubkey)
        session_dict = {'SessionKey':uuid.uuid1().hex,'nonce':randint(9180483,999999239992399)}
        print("Before Connection..\n")
        print(session_dict)
        nonce = session_dict['nonce']
        self.session_id = session_dict['SessionKey']
        encrypted = encryptor.encrypt(bytes(str(session_dict),'utf-8'))
        PARAMS={'packet':encrypted}
        print("Encrypted Session Key and nonce: \n")
        print(PARAMS)
        self.send(encrypted, msg_type=MessageType.AUTH_ACK)
        response = self.recv()['data'] #requests.get("http://localhost:5000/public_key_exchange_api/connect",json={"packet": str(encrypted)})
        print("After connection..\n")
        print(response)
        if int(response) == (nonce+1):
            return True
        else:
            print("Incorrect Nonce Recieved\n")
            return False

    def upload(self, file):
        self.send(open(file, 'rb').read(), msg_type=MessageType.UPLOAD, extra=file.split("/")[-1])


def read_file():
    byte_list = []
    with open('test.png', 'rb') as f:
        while True:
            byte_s = f.read(1)
            if not byte_s:
                break
            byte_list.append(byte_s)

if __name__=='__main__':
    # read_file()
    client = AuthClient()
    authenticated = False
    while True:
        print_menu()
        choice = input("Please enter your choice: ")
        if int(choice) == 1 and client.auth():
            authenticated = True
            print("Connected!\n")
        elif int(choice) == 2 and authenticated:
            file_path = input("File path ?")
            if os.path.exists(file_path):
                client.upload(file_path)
        else:
            break
