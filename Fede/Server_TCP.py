from socket import *

connectionSocket = 0


def main():
    connectionSocket = StartConnection()

    while True:
        x = MenuOperativo()
        InviaSelezioneMenu(x, connectionSocket)
        if x == "0":
            break

    StopConnection(connectionSocket)


def MenuOperativo():

    # aggiungere controlli nel caso
    while True:
        x = 0
        print('cosa vuoi fare?')
        print('inserisci 1 per ricevere info Sistema Operativo')
        print('inserisci 2 per gestire la shell')
        print('inserisci 3 per fare una ricerca')
        print('inserisci 4 per scaricare un file')
        print('inserisci 0 per fermare la connessione')

        x = input()
        if x == "0":
            return "0"
        elif x == "1" or x == "2" or x == "3" or x == "4":
            return x;
        else:
            x = 0

    return x


def InviaSelezioneMenu(x, connectionSocket):
    connectionSocket.send(x.encode())
    print(connectionSocket.recv(4).decode())


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

        if (addr):
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
