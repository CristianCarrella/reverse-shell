import time
from socket import *
import pyautogui, sys
serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
print ('The server is ready to receive')
connectionSocket, addr = serverSocket.accept()
while True:
    x, y = pyautogui. position()
    print(x.__str__() + " " + y.__str__())
    connectionSocket.send(str(x).encode())
    connectionSocket.send(str(y).encode())
    connectionSocket.recv(2)
connectionSocket.close()