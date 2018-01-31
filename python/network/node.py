"""
Server/Client Node
"""
import socket
import threading
import struct

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
                t = threading.Thread(target=self.handle_peer, args=[c_s])
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

    def handle_peer(self, client_socket):
        """
        .
        """
        host, port = client_socket.getpeername()
        peer = NodeConnection(None, host, port, client_socket)
        try:
            mtype, mdata = peer.recv()
            self.handlers[mtype](peer, mdata)
        except KeyboardInterrupt:
            raise
        peer.close()

    def find_host(self):
        """
        locate hostname of this node
        """
        s = socket.socket()
        s.connect(("www.google.com", 80))
        self.host = s.getsockname()[0]
        s.close()


class NodeConnection:

    def __init__(self, name, host, port, sock=None):
        self.name = name
        if not sock:
            self.s = socket.socket()
            self.s.connect((host, port))
        else:
            self.s = sock
        self.sd = self.s.makefile('rw', 0)

    def makemsg(self, mtype, mdata):
        mlen = len(mdata)
        msg = struct.pack("!4sL%ds" % mlen, mtype, mlen, mdata)
        return msg

    def send(self, mtype, mdata):
        try:
            msg = self.makemsg(mtype, mdata)
            self.sd.write(msg)
            self.sd.flush()
        except KeyboardInterrupt:
            raise
        return True

    def recv(self):
        try:
            mtype = self.sd.read(4)
            lenstr = self.sd.read(4)
            mlen = int(struct.unpack("!L", lenstr)[0])
            msg = ""
            while len(msg) != mlen:
                data = self.sd.read(min(2048, mlen - len(msg)))
                if not len(data):
                    break
                msg += data
            if len(msg) != mlen:
                return (None, None)
        except KeyboardInterrupt:
            raise
        return (mtype, msg)

    def close(self):
        self.s.close()
        self.s = None
        self.sd = None
