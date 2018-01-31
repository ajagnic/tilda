"""
Server/Client Node
"""
import socket
import threading

__version__ = '0.0.1'
__author__ = 'Adrian Agnic'


class Node:

    def __init__(self, port, maxPeers=0, name=None, host=None):
        """
        :type port: int
        :type host: str
        :param maxPeers: max connections held
        :param name: unique identifier
        """
        self.port = port
        self.maxPeers = maxPeers
        self.peers = {}
        self.stop = False
        self.handlers = {}
        self.router = None
        if host:
            self.host = host
        else:
            self.find_host()
        if name:
            self.name = name
        else:
            self.name = "{}:{}".format(self.host, self.port)

    def listen_connections(self):
        """
        main loop
        """
        s = self.server_socket(self.port)
        s.settimeout(2)
        while not self.stop:
            try:
                c_s, c_addr = s.accept()
                c_s.settimeout(None)
                t = threading.Thread(target=self.handlepeer, args=[c_s])
                t.start()
            except KeyboardInterrupt:
                self.stop = True
                continue
        s.close()

    def server_socket(self, port, backlog=5):
        """ open socket for incoming connections
        :param port: int: port to bind to
        :param backlog: int: amount of connections to accept before refuse
        :return: socket obj
        """
        s = socket.socket()
        # SOL_SOCKET == socket layer, SO_REUSEADDR, 1 == re-use port on socket close
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # IPv4 address tuple empty string == ADDR_ANY
        s.bind(('', port))
        s.listen(backlog)
        return s

    def find_host(self):
        """
        locate host of this node
        """
        pass
