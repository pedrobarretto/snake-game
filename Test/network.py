import socket
import json
import pickle

class Network:

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.client.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 8192)
        self.host = '127.0.0.1'
        self.port = 32016
        self.addr = (self.host, self.port)
        self.id = self.connect()

    def connect(self):
        self.client.connect(self.addr)
        # return self.client.recv(2048)
        return pickle.loads(self.client.recv(1000000000000))

    def send(self, data):
        """
        :param data: json
        :return: str
        """
        try:
            print('network data: ', data)
            self.client.sendall(pickle.dumps(data))
            reply = pickle.loads(self.client.recv(1000000000000))
            print('network reply: ', reply)
            return reply
        except socket.error as e:
            return str(e)
