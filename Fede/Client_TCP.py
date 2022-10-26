from socket import *
import platform

def main():
    clientSocket = StartConnection()
    sendOsInfo(clientSocket)
    StopConnection(clientSocket)

def sendOsInfo(clientSocket):
    pack = "Architecture: " + platform.architecture()[
        0] + "\nMacchine: " + platform.machine() + "\nSystem name: " + platform.system()
    pack = pack + "\nOperating system release: " + platform.release() + "\nOperating system version: " + platform.version() + "\nNode: " + platform.node() + "\nPlatform: " + platform.platform() + "\nProcessor: " + platform.processor()
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

def MenuOperativo():
    x=0
    print('cosa vuoi fare?')
    print('inserisci 1 per ricevere info Sistema Operativo')
    print('inserisci 2 per gestire la shell')
    print('inserisci 3 per fare una ricerca')
    print('inserisci 4 per scaricare un file')
    print('inserisci 0 per fermare la connessione')
    input(x)
    return x


if __name__ == '__main__':
    main()

#probabilmente si puo risolvere il problema dei pacchetti alternando sempre .send e . recv
#implementare error 404
