import os
import socket
from threading import Thread

RECV_SIZE= 4096
CLIENT_ADRS= '127.0.0.1'
SERVER_ADRS= '127.0.0.1'
MASTER_PORT= 1234
PORT_SPACE_LOWER= 2000
PORT_SPACE_UPPER= 9000

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
            data= self.client.recv(RECV_SIZE)
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
            data= self.server.recv(RECV_SIZE)
            if data:
                print("[{}] -> {}".format(self.port, data[:100].encode('hex')))
                self.client.sendall(data)

class Proxy(Thread):

    def __init__(self, client_adrs, server_adrs, port):
        super(Proxy, self).__init__()
        self.client_adrs= client_adrs
        self.server_adrs= server_adrs
        self.port= port

    def run(self):
        while True:
            print("[proxy({})] being set up".format(self.port))
            self.c2p= Client2Proxy(self.client_adrs, self.port)
            self.p2s= Proxy2Server(self.server_adrs, self.port)
            print("[proxy({})] connection established".format(self.port))
            self.c2p.server= self.p2s.server
            self.p2s.client= self.c2p.client

            self.c2p.start()
            self.p2s.start()

class MasterServer(Thread):
    availablePorts= []
    aux_servers= []

    def allocate_aux_server(self, port):
        _aux_server= Proxy(CLIENT_ADRS, SERVER_ADRS, port)
        _aux_server.start()
        self.aux_servers.append(_aux_server)

    def __init__(self):
        
        aggregator= Proxy(CLIENT_ADRS, SERVER_ADRS, MASTER_PORT)
        
        portsCount= PORT_SPACE_UPPER - PORT_SPACE_LOWER
        for currentPort in range(portsCount):
            _available_port= PORT_SPACE_LOWER + currentPort
            self.availablePorts.append(_available_port)

        self.allocate_aux_server(5005)



    # def run(self):
    #     thread.start_new_thread(run_interface,())
    
    #console thread
    def run_interface(self):
        while True:
            # try:
            cmd= input('$ ')
            if cmd[:4] == 'exit' or 'quit':
                os._exit(0)
            # except Exception e:
            #     print e


print('dsads')
master_server= MasterServer()