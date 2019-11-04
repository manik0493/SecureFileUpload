import threading
import json
import sys
sys.path.append('../shared')
from message_type import MessageType

class BaseClientHandler(object):
    INIT = 0
    START = 1
    FINISHED = 2

class ClientHandler(BaseClientHandler):
    def __init__(self, socket, address):
        self.socket = socket
        self.address = address
        self.status = self.INIT
        self.thread = None

    def start(self):
        self.thread = threading.Thread(target=self.msg_handler)
        self.thread.start()
        self.status = self.START

    # return False to break connection
    def _process_msg(self, data):
        connection = self.socket
        if data == b"<TERMINATE>":
            print("Client closing connection. Closing socket")
            return False
        else:
            print( 'received "%s"' % data)
            if data:
                print( 'sending data back to the client')
                self._send(data)

            else:
                print( 'no more data from', client_address)
                return False
        return data

    def msg_handler(self):
        try:
            print( 'connection from', self.address)

            # Receive the data in small chunks and retransmit it
            while True:
                data = self._recv()
                if not self._process_msg(data):
                    break
        # except:
            # print("Error occured, closing client socket")
        finally:
            self.status = self.FINISHED
            # Clean up the connection
            self.socket.close()

    def _recv(self):
        socket = self.socket
        msg_size = int(socket.recv(16))

        amount_received = 0
        amount_expected = msg_size

        complete_data = b''
        while amount_received < amount_expected:
            data = socket.recv(min([1024, amount_expected - amount_received]))
            amount_received += len(data)
            print( 'received "%s"' % data)
            complete_data += data


        return complete_data

    def _send(self, msg):
        socket = self.socket
        print( 'sending "%s"' % msg)
        if type(msg) != bytes:
            msg = msg.encode()
        msg_size = len(msg)
        socket.sendall(str(msg_size).rjust(16).encode())
        socket.sendall(msg)

class JSONClientHandler(ClientHandler):
    def __init__(self, socket, address):
        super().__init__(socket, address)

    def _recv(self):
        return json.loads(super()._recv())

    def _send(self, msg, msg_type=0):
        # if not self._is_json(msg):
        msg = json.dumps({"data": str(msg), "type": msg_type})
        super()._send(socket, msg)

    def _process_msg(self, data):
        if data['type'] == MessageType.TERMINATE:
            print("Client closing connection. Closing socket")
            return False
        # self._send(connection, data)
        return data

    def _is_json(self, json_msg):
      try:
        json_object = json.loads(json_msg)
      except:
        return False
      return True
