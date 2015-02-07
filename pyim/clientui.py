from sys import *

from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from client import *

class ClientUI(QWidget):
    def __init__(self):
        super(ClientUI, self).__init__()
        
        #client stuff
        self.client = Client()
        
        #GUI stuff
        ipLabel = QLabel("IP:")
        portLabel = QLabel("Port:")
        nameLabel = QLabel("Name:")
        
        self.ipText = QLineEdit()
        self.ipText.setPlaceholderText("localhost")
        self.portText = QLineEdit()
        self.portText.setPlaceholderText("2015")
        self.nameText = QLineEdit()
        self.nameText.setPlaceholderText("Default Name")
        self.connectButton = QPushButton("Connect")
        self.connectButton.clicked.connect(self.connect)
        
        self.text = QTextEdit()
        self.inputText = QLineEdit()
        self.inputText.setPlaceholderText("Enter your message here")
        self.inputText.editingFinished.connect(self.handleInput)
        
        #add the components
        top = QFrame()
        lay1 = QHBoxLayout()
        lay1.addWidget(ipLabel)
        lay1.addWidget(self.ipText)
        lay1.addWidget(portLabel)
        lay1.addWidget(self.portText)
        lay1.addWidget(nameLabel)
        lay1.addWidget(self.nameText)
        lay1.addWidget(self.connectButton)
        top.setLayout(lay1)
        
        mid = QFrame()
        lay2 = QHBoxLayout()
        lay2.addWidget(self.text)
        mid.setLayout(lay2)
        
        bot = QFrame()
        lay3 = QHBoxLayout()
        lay3.addWidget(self.inputText)
        bot.setLayout(lay3)
        
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(top)
        mainLayout.addWidget(mid)
        mainLayout.addWidget(bot)
        self.setLayout(mainLayout)
        self.setWindowTitle("PyIM Client")
    
    def connect(self):
        ip = self.ipText.text()
        portTxt = self.portText.text()
        name = self.nameText.text()
        
        if ip == "":
            ip = "localhost"
        if portTxt == "":
            portTxt = "2015"
        if name == "":
            name = "Default Name"
        
        port = int(portTxt)
        self.client.connect(ip, port, name)
        print("Connected to", ip + ":" + str(port))
    
    def handleInput(self):
        text = self.inputText.getText()
        
        if text == "": return
        
        self.inputText.setText("")
    
    def closeEvent(self, event):
        event.accept()

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    cui = ClientUI()
    cui.show()
    
    sys.exit(app.exec_())