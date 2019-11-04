import socket
import sys
from client_handlers import ClientHandler, JSONClientHandler

class BaseServer(object):
    def __init__(self, address='localhost', port=10000):
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.handlers = []
        self.address = address
        self.port = port
        self.client_handler = ClientHandler

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
            handler = self.client_handler(connection, client_address)
            self.handlers.append(handler)
            handler.start()

    def send_all(self, msg):
        finished_handlers = []
        for handler in handlers:
            if handler.status != ClientHandler.FINISHED:
                handler._send(msg)
            else:
                finished_handlers.append(handler)

        handlers = list(set(handlers) - set(finished_handlers))

    def stop(self):
        self.sock.close()

class JSONServer(BaseServer):
    def __init__(self, address='localhost', port=10000):
        super().__init__(address, port)
        self.client_handler = JSONClientHandler

if __name__ == '__main__':
    server = JSONServer()
    server.start()
    server.stop()
