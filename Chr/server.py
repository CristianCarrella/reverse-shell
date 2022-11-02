from socket import *
 
 
def receiveDir(connectionSocket):
    outputSize = int(connectionSocket.recv(1024).decode())
    connectionSocket.send("OK".encode())
    out = connectionSocket.recv(outputSize).decode()
    print(out)
 
 
def exitNClose(connectionSocket, cmd):
    connectionSocket.send(cmd.encode())
    out = connectionSocket.recv(1024).decode()
    return True
 
 
def changeDirectory(connectionSocket):
    out = connectionSocket.recv(1024).decode()
    print(out)
 
 
def getFile(connectionSocket, fileName):
    fileSize = int(connectionSocket.recv(1024).decode())
    file = open(fileName, 'wb')
    while fileSize > 0:
        if fileSize < 1024:
            out = connectionSocket.recv(fileSize)
        else:
            out = connectionSocket.recv(1024)
        fileSize = fileSize - 1024
        file.write(out)
        print("Ricevendo...")
    print("Ricevuto")
    file.close()
 
 
def main():
    serverPort = 12003
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', serverPort))
    serverSocket.listen(1)
    print('The server is ready to receive')
    connectionSocket, addr = serverSocket.accept()
    print('Accepted a new client', addr)
    esc = False
    while not esc:
        cmd = input('>>')
        connectionSocket.send(cmd.encode())

        #check se linux o windows
        if cmd == "dir" or "ls" in cmd:
            receiveDir(connectionSocket)
 
        elif cmd == "esc":
            esc = exitNClose(connectionSocket, cmd)
 
        elif "cd" in cmd:
            changeDirectory(connectionSocket)
 
        elif "get" in cmd:
            fileName = cmd.replace("get ", "")
            existFile = connectionSocket.recv(1024).decode()
            if existFile == "ok":
                getFile(connectionSocket, fileName)
            else:
                print("File not found")
 
    connectionSocket.close()
 
 
if __name__ == "__main__":
    main()
