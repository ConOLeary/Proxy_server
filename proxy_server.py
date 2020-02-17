import socket
from threading import Thread

recvSize= 4096
fromAdrs= '127.0.0.1'
toAdrs= '127.0.0.1'
defaultPort= 1234
portSpaceLower= 3000
portSpaceUpper= 3009

class Client2Proxy(Thread):

    def __init__(self, host, port):
        super(Client2Proxy,self).__init__()
        self.server= None
        self.port= port
        self.host= host
        sock= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        sock.listen(1)
        #thread waits
        self.client, addr= sock.accept()

    #to be threaded
    def run(self):
        while True:
            data= self.client.recv(recvSize)
            if data:
                print("[{}] -> {}".format(self.port, data[:100].encode('hex')))
                self.server.sendall(data)

class Proxy2Server(Thread):

    #set up connection
    def __init__(self, host, port):
        super(Proxy2Server, self).__init__()
        self.client= None
        self.port= port
        self.host= host
        self.server= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((host, port))

    #to be threaded
    def run(self):
        while True:
            data= self.server.recv(recvSize)
            if data:
                print("[{}] -> {}".format(self.port, data[:100].encode('hex')))
                self.client.sendall(data)

class Proxy(Thread):

    def __init__(self, from_host, to_host, port):
        super(Proxy, self).__init__()
        self.from_host= from_host
        self.to_host= to_host
        self.port= port

    def run(self):
        while True:
            print("[proxy({})] being set up".format(self.port))
            self.c2p= Client2Proxy(self.from_host, self.port)
            self.p2s= Proxy2Server(self.to_host, self.port)
            print("[proxy({})] connection established".format(self.port))
            self.c2p.server= self.p2s.server
            self.p2s.client= self.c2p.client

            self.c2p.start()
            self.p2s.start()

print('dsads')
main_server= Proxy(fromAdrs, toAdrs, defaultPort)

for port in range(portSpaceLower, portSpaceUpper):
    aux_server= Proxy(fromAdrs, toAdrs, port)
    aux_server.start()