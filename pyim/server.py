import socket
import select
from threading import Thread

from packet import *

class Server:
    """
    
    """
    
    def __init__(self, host = "localhost", port = 2015):
        self.clients = []
        self.numIds = 0
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))
        self.socket.listen(10)
        self.socket.settimeout(1)
        
        print("Server listening on port", port)
        
        while True:
            try:
                (clientsocket, address) = self.socket.accept()
            except socket.timeout:
                continue
            
            print("Client connected from", address)
            self.numIds += 1
            c = Client(sock = clientsocket, addr = address, sv = self, id = self.numIds)
            ct = Thread(target=c.run)
            ct.start()
            self.clients.append(c)
            
            tmpList = list(self.clients)
            
            for cli in tmpList:
                if not cli.connected:
                    self.clients.remove(cli)
    
    def broadcast(self, packet):
        for cli in self.clients:
            cli.socket.sendall(packet)

class Client:
    """
    The server's instance of a client
    """
    def __init__(self, sock = None, addr = None, sv = None, id = 0, nm = "Default Name"):
        self.socket = sock
        self.address = addr
        self.server = sv
        self.id = id
        self.connected = True
        
        self.name = nm
    
    def run(self):
        #get the initial sending of the client's name
        self.socket.settimeout(5)
        try:
            namePacket = self.socket.recv(1024)
        
            if namePacket == b"":
                print("Socket error. Closing connection")
                self.connected = False
            elif namePacket[0] == 2:
                self.name = namePacket[3:].decode("utf-8")
            
            self.socket.settimeout(None)
            
            #send client their id
            self.socket.sendall(str(self.id).encode("utf-8"))
        except socket.timeout:
            print("Didn't receive name from client. Closing connection")
            self.connected = False
        
        #main client loop
        while self.connected:
            tmp = self.socket.recv(2048)
            
            if tmp == b"" or not self.handle_packet(tmp):
                self.connected = False
        
        self.socket.close()
        print("Client connection closed for", self.address)

    def handle_packet(self, packet):
        flag = packet[0]
        src = packet[1:2]
        dst = packet[2:3]
        data = packet[3:]
        
        if flag == 1:
            print(self.name + ">", data.decode("utf-8"))
            self.server.broadcast(ID_MSG + self.get_id() + b"\0" + data)
            return True
        elif flag == 2:
            print(self.name, "set new name", end=" ")
            self.name = data.decode("utf-8")
            print(self.name)
            self.server.broadcast(ID_NAME + self.get_id() + b"\0" + data)
            return True
        else:
            print("Unknown packet received")
            return False
    
    def get_id(self):
        return str(self.id).encode("utf-8")

if __name__ == "__main__":
    server = Server()