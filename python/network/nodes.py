import socket
import threading

__author__='Adrian Agnic'
__version__='0.0.1'


class Mother:

    __slots__=['host','port','s','ips','maxPeers']

    def __init__(self, maxPeers=0):
        self.host="127.0.0.1"
        self.port=5999
        self.s=None
        self.ips=[]
        self.maxPeers=maxPeers

    def up(self):
        self.s=socket.socket()
        self.s.bind((self.host,self.port))
        self.s.listen(self.maxPeers)
        while True:
            s, addr=self.s.accept()
            self.ips.append(addr)
            print("New IP: {}".format(str(addr)))
            t=threading.Thread(target=self.recv,args=[s])
            t.daemon=True
            t.start()

    def recv(self, s):
        while True:
            data=s.recv(1024).decode()
            if not data:
                break
            print(data)
        s.close()

    def peers(self):
        return self.ips

    def down():
        self.s.close()

class Node:
    def __init__(self):
        self.remhost='127.0.0.1'
        self.remport=5999

    def up(self):
        self.s=socket.socket()
        self.s.connect((self.remhost,self.remport))
        msg="Hello World"
        self.s.send(msg.encode())
        self.s.close()
