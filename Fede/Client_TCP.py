from socket import *
import platform


def main():
    clientSocket = StartConnection()

    RiceviMenu(clientSocket)
    print("uscito")

    StopConnection(clientSocket)

def RiceviMenu(clientSocket):

    while True:
        x = clientSocket.recv(2).decode()
        clientSocket.send("k".encode())
        if x == "1":
            print("ricevere info Sistema Operativo")
        if x == "2":
            print("gestire la shell")
        if x == "3":
            print("fare una ricerca")
        if x == "4":
            print("scaricare un file")
        if x == "0":
            break #chiudi la connessione


def sendOsInfo(clientSocket):
    pack = "Architecture: " + platform.architecture()[
        0] + "\nMacchine: " + platform.machine() + "\nSystem name: " + platform.system()
    pack = pack + "\nOperating system release: " + platform.release() + "\nOperating system version: " + \
           platform.version() + "\nNode: " + platform.node() + "\nPlatform: " + platform.platform() + "\nProcessor: " + platform.processor()
    clientSocket.send(pack.encode())


def StartConnection():
    serverName = 'localhost'
    serverPort = 12001
    clientSocket = socket(AF_INET, SOCK_STREAM)

    clientSocket.connect((serverName, serverPort))

    return clientSocket


def StopConnection(clientSocket):
    modifiedSentence = clientSocket.recv(1024)
    print('From Server:', modifiedSentence.decode())
    clientSocket.close()


if __name__ == '__main__':
    main()

# probabilmente si puo risolvere il problema dei pacchetti alternando sempre .send e . recv
# implementare error 404
