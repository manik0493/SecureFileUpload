import socket
import threading
import sys
sys.path.append('../shared')
from message_type import MessageType

class BaseServer(object):
    def __init__(self, address='localhost', port=10000):
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.threads = []
        self.connections = []
        self.address = address
        self.port = port

    def start(self):
        # Bind the socket to the port
        server_address = (self.address, self.port)
        print('starting up on %s port %s' % server_address)
        self.sock.bind(server_address)

        # Listen for incoming connections
        self.sock.listen(10)
        self.client_thread_dispatcher()

    def client_thread_dispatcher(self):
        print( 'waiting for a connection')
        while True:
            connection, client_address = self.sock.accept()
            self.connections.append(connection)
            thread = threading.Thread(target=self.msg_handler, args=(connection, client_address))
            self.threads.append(thread)
            thread.start()
        # self.msg_handler(connection, client_address)

    # return False to break connection
    def _process_msg(self, connection, data):
        if data == b"<TERMINATE>":
            print("Client closing connection. Closing socket")
            return False
        else:
            print( 'received "%s"' % data)
            if data:
                print( 'sending data back to the client')
                self._send(connection, data)

            else:
                print( 'no more data from', client_address)
                return False
        return data

    def msg_handler(self, connection, client_address):
        try:
            print( 'connection from', client_address)

            # Receive the data in small chunks and retransmit it
            while True:
                data = self._recv(connection)
                if not self._process_msg(connection, data):
                    break
        # except:
            # print("Error occured, closing client socket")
        finally:
            self.connections.remove(connection)
            # Clean up the connection
            connection.close()

    def send_all(self, msg):
        for connection in connections:
            _sent(connection, msg)

    def _recv(self, socket):
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

    def _send(self, socket, msg):
        print( 'sending "%s"' % msg)
        if type(msg) != bytes:
            msg = msg.encode()
        msg_size = len(msg)
        socket.sendall(str(msg_size).rjust(16).encode())
        socket.sendall(msg)

    def stop(self):
        self.sock.close()

import json
class JSONServer(BaseServer):
    def __init__(self, address='localhost', port=10000):
        super().__init__(address, port)

    def _send(self, socket, msg, msg_type=0):
        # if not self._is_json(msg):
        msg = json.dumps({"data": str(msg), "type": msg_type})
        super()._send(socket, msg)

    def _recv(self, socket):
        return json.loads(super()._recv(socket))

    def _process_msg(self, connection, data):
        if data['type'] == MessageType.TERMINATE:
            print("Client closing connection. Closing socket")
            return False
        else:
            print( 'received "%s"' % data)
            if data:
                print( 'sending data back to the client')
                self._send(connection, data)

            else:
                print( 'no more data from', client_address)
                return False
        return data

    def _is_json(self, json_msg):
      try:
        json_object = json.loads(json_msg)
      except:
        return False
      return True

if __name__ == '__main__':
    server = JSONServer()
    server.start()
    server.stop()
