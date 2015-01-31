import sys
import socket
from threading import Thread

from packet import *

class Client:
    """
    Simple test client
    """
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(1)
        self.run = True
        self.thread = Thread(target=self.read, args=())
        self.thread.start()
        
        self.id = 0
        self.names = {}
        """
        self.connect()
        
        while self.run:
            line = input("> ")
            self.handle_input(line)
        
        self.close()"""
    
    def connect(self, host = "localhost", port = 2015, name = "Default Name"):
        try:
            self.name = name
            self.sock.connect((host, port))
            self.sock.sendall(NAME_FLAG + self.name.encode("utf-8"))
            tmp = self.sock.recv(4).decode("utf-8")
            self.id = int(float(tmp))
            print("my id:", self.id)
            self.names[self.id] = self.name
        except:
            print("Error connecting to server: ", sys.exc_info()[0])
    
    def disconnect(self):
        self.run = False
    
    def handle_input(self, line):    
        #if chat command
        if line[0] == '/':
            self.handle_command(line[1:])
        #it's a message
        else:
            self.sock.sendall(MSG_FLAG + line.encode("utf-8"))

    def handle_command(self, cmd):
        if cmd == "help":
            print("-----===== PyIM Help =====-----")
        elif str.find(cmd, "setname") == 0:
            self.name = cmd[8:]
            self.sock.sendall(NAME_FLAG + cmd[8:].encode("utf-8"))
    
    def send(self, packet):
        res = self.sock.sendall(packet)
        if res == 0:
            raise RuntimeError("socket connection broken")
    
    def read(self):
        while self.run:
            try:
                data = self.sock.recv(2048)
            except socket.timeout:
                continue
            
            self.handle_packet(data)
    
    def handle_packet(self, packet):
        flag = packet[0]
        data = packet[1:]
        
        if flag == 1:
            print(self.name + ">", data.decode("utf-8"))
            return True
        elif flag == 2:
            print("setting new name")
            self.name = data.decode("utf-8")
            return True
        else:
            print("Unknown packet received")
            return False

if __name__ == "__main__":
    client = Client()