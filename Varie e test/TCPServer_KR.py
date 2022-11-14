from socket import *


def receiveDirNTreeOutput(connectionSocket):
    outputSize = int(connectionSocket.recv(1024).decode())
    out = connectionSocket.recv(outputSize).decode()
    print(out)


def exitNClose(connectionSocket, cmd):
    connectionSocket.send(cmd.encode())
    out = connectionSocket.recv(1024).decode()
    return True


def changeDirectory(connectionSocket):
    out = connectionSocket.recv(1024).decode()
    print(out)


def getFile(connectionSocket, fileName, fileSize):
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
    serverPort = 12000
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

        if cmd == "dir" or cmd == "tree":
            receiveDirNTreeOutput(connectionSocket)

        elif cmd == "esc":
            esc = exitNClose(connectionSocket, cmd)

        elif "cd" in cmd:
            changeDirectory(connectionSocket)

        elif "get" in cmd:
            fileSize = int(connectionSocket.recv(1024).decode())
            fileName = cmd.replace("get ", "")
            getFile(connectionSocket, fileName, fileSize)

    connectionSocket.close()


if __name__ == "__main__":
    main()
