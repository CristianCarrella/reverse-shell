from socket import *
connectionSocket = 0

def main():
    connectionSocket = StartConnection()
    StopConnection(connectionSocket)


def StartConnection():
    print('opening the server \n')
    serverPort = 12001
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', serverPort))
    serverSocket.listen(1)
    print('Server Ready')
    while True:
        connectionSocket, addr = serverSocket.accept()
        print('Connesso', addr)

        sentence = connectionSocket.recv(1024).decode()
        print(sentence)

        if(addr):
            break

    return connectionSocket


def StopConnection(connectionSocket):
    print('stopping the connection')
    if connectionSocket:
        connectionSocket.send(("end").encode())
        print("End")
        connectionSocket.close()


if __name__ == '__main__':
    main()
