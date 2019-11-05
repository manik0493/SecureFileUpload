# from flask import Flask
# from apis import api
from core import Configs
from Crypto.PublicKey import RSA
from socket_server import JSONServer
from client_handlers import JSONClientHandler
import sys
sys.path.append('../shared')
from message_type import MessageType
from Crypto.Cipher import PKCS1_OAEP
import ast

class AuthClientHandler(JSONClientHandler):
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
            nonce = int(session_dict['nonce'])
            Configs.CLIENT_SESSION_BOOK[session_dict['SessionKey']] = 0
            self._send(str(nonce+1), msg_type=MessageType.AUTH_FIN)
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

    server = AuthServer()
    server.start()
    server.stop()

# app = Flask(__name__)
# api.init_app(app)

# app.run(debug=True)
