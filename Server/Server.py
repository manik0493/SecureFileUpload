# from flask import Flask
# from apis import api
from core import Configs
from Crypto.PublicKey import RSA
from socket_server import JSONServer
from client_handlers import JSONClientHandler
import sys, hashlib, itertools
from Crypto.Cipher import PKCS1_OAEP
import ast

sys.path.append('../shared')
from message_type import MessageType
import encryption_utils

class AuthClientHandler(JSONClientHandler):
    def __init__(self, socket, address):
        super().__init__(socket, address)
        self.decrypt_map = {}

    def _process_msg(self, data):
        data = super()._process_msg(data)
        if not data:
            return False

        if data['type'] == MessageType.AUTH_REQ:
            self._send(open(Configs.PUBLIC_KEY_FILE,'rb').read(), msg_type=MessageType.AUTH)

        if data['type'] == MessageType.AUTH_ACK:
            decryptor = PKCS1_OAEP.new(Configs.PUBLIC_KEY_OBJECT)
            decrypted = decryptor.decrypt(ast.literal_eval(str(data['data']))).decode('utf-8')
            session_dict =ast.literal_eval(decrypted)
            self.session_key = session_dict['SessionKey']
            nonce = int(session_dict['nonce'])
            self.decrypt_map = encryption_utils.generate_decrypt_map(self.session_key, data_size=2)
            # Configs.CLIENT_SESSION_BOOK[session_dict['SessionKey']] = 0
            self._send(str(nonce+1), msg_type=MessageType.AUTH_FIN)

        if data['type'] == MessageType.UPLOAD:
            encrypted_file_content = data['data']
            filename = data['extra']
            file_content = encryption_utils.decrypt(encrypted_file_content, self.decrypt_map)

            if type(file_content) == str:
                with open(filename, 'w') as f:
                    f.write(file_content)
            else:
                with open(filename, 'wb') as f:
                    f.write(file_content)

        if data['type'] == MessageType.DOWNLOAD_REQ:
            filename = data['data']
            file_contents = open(filename, 'rb').read()
            file_contents = encryption_utils.encrypt(file_contents, self.session_key)
            self._send(file_contents, msg_type=MessageType.DOWNLOAD, extra=filename.split("/")[-1])

        return data

class AuthServer(JSONServer):
    def __init__(self, address='localhost', port=10000):
        super().__init__(address, port)
        self.client_handler = AuthClientHandler


if __name__ == '__main__':
    pub_key =RSA.generate(1024)
    f = open('mykey.pem','wb')
    f.write(pub_key.publickey().export_key('PEM'))
    f.close()
    Configs.PUBLIC_KEY_FILE = 'mykey.pem'
    Configs.PUBLIC_KEY_OBJECT = pub_key
    Configs.CLIENT_SESSION_BOOK = {}

    server = AuthServer(port=10001)
    server.start()
    server.stop()

# app = Flask(__name__)
# api.init_app(app)

# app.run(debug=True)
