import socket
import sys
import time
sys.path.append('../shared')
from message_type import MessageType

class BaseClient(object):
    def __init__(self, address, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect the socket to the port where the server is listening
        server_address = (address, port)
        print('connecting to %s port %s' % server_address)
        self.sock.connect(server_address)


    def send(self, msg):
        # print( 'sending "%s"' % msg)
        if type(msg) != bytes:
            msg = msg.encode()
        msg_size = len(msg)
        self.sock.sendall(str(msg_size).rjust(16).encode())
        self.sock.sendall(msg)

    def recv(self):
        msg_size = int(self.sock.recv(16))

        amount_received = 0
        amount_expected = msg_size

        complete_data = b''
        while amount_received < amount_expected:
            data = self.sock.recv(min([1024, amount_expected - amount_received]))
            amount_received += len(data)
            # print( 'received "%s"' % data)
            complete_data += data
        return complete_data

    def stop(self):
        self.send("<TERMINATE>")
        self.sock.close()

import json
class JSONClient(BaseClient):
    def __init__(self, address, port):
        super().__init__(address, port)

    def send(self, msg, msg_type=0, extra=None):
        # if not self._is_json(msg):
        msg = {"data": str(msg), "type": msg_type}
        if extra is not None:
            msg['extra'] = extra
        msg = json.dumps(msg)
        super().send(msg)

    def recv(self):
        data = json.loads(super().recv())
        try:
            data['data'] = eval(data['data'])
            data['data'] = data['data'].decode()
        except Exception as e:
            pass
        return data

    def _is_json(self, json_msg):
      try:
        json_object = json.loads(json_msg)
      except ValueError as e:
        return False
      return True

    def stop(self):
        self.send("", msg_type=MessageType.TERMINATE)
        time.sleep(0.5)
        self.sock.close()


if __name__ == '__main__':
    client = JSONClient('localhost', 10000)
    message = input()
    client.send(message)
    # print(client.recv())
    client.stop()
