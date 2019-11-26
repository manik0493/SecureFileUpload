# from flask import Flask
# from apis import api
from core import Configs
from Crypto.PublicKey import RSA
from socket_server import JSONServer
from client_handlers import JSONClientHandler
import sys, hashlib, itertools
sys.path.append('../shared')
from message_type import MessageType
from Crypto.Cipher import PKCS1_OAEP
import ast

class AuthClientHandler(JSONClientHandler):
    def __init__(self, socket, address):
        super().__init__(socket, address)
        self.decrypt_map = {}

    def fill_decrypt_map(self, key, data_size):
        key = ''

        chrset = [ x for x in range(0, 256) ]
        perms = itertools.product(chrset, repeat=data_size)
        for perm in perms:
            dec = bytes(perm)
            # print(key, chr(perm))
            enc = hashlib.sha1(key.encode() + dec).digest()
            # if dec=='RI' or dec == b'RI':
            print(dec, enc)
            self.decrypt_map[enc] = dec
        # print(self.decrypt_map)

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
            self.fill_decrypt_map(self.session_key, data_size=2)
            # Configs.CLIENT_SESSION_BOOK[session_dict['SessionKey']] = 0
            self._send(str(nonce+1), msg_type=MessageType.AUTH_FIN)

        if data['type'] == MessageType.UPLOAD:
            def chunks(l, n):
                """Yield successive n-sized chunks from l."""
                for i in range(0, len(l), n):
                    yield l[i:i + n]


            encrypted_file_content = data['data']
            filename = data['extra']

            file_contents = []
            for encrypted_chunk in chunks(encrypted_file_content, 20):
                # print(len(file_contents), file_contents)
                file_contents.append(self.decrypt_map[encrypted_chunk])

            file_content = b''.join(file_contents)

            if type(file_content) == str:
                with open(filename, 'w') as f:
                    f.write(file_content)
            else:
                with open(filename, 'wb') as f:
                    f.write(file_content)
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

    server = AuthServer(port=10000)
    server.start()
    server.stop()

# app = Flask(__name__)
# api.init_app(app)

# app.run(debug=True)
