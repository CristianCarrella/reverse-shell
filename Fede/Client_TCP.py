from socket import *
import platform
import time


def main():
    while True:
        try:
            clientSocket = StartConnection()  # apre connessione

            RiceviMenu(clientSocket)  # aspetta la ricezione del da farsi
            # va in loop e non esce fin quando non si inserisce zero

            StopConnection(clientSocket)  # chiude la connessione e termina
            break
        except:
            print("errore Riavvio in corso")
            clientSocket.close()

def RiceviMenu(clientSocket):  # riceve il menù e fa partire i vari metodi
    while True:
        x = clientSocket.recv(2).decode()
        clientSocket.send("k".encode())  # conferma (da rimuovere)!

        if x == "1":
            print("ricevere info Sistema Operativo")
            sendOsInfo(clientSocket)

        if x == "2":
            print("gestire la shell")
            # metti qui la tua chiamata per la shell

        if x == "3":
            print("fare una ricerca")
            # metti qui la tua chiamata per la ricerca

        if x == "4":
            print("scaricare un file")
            # metti qui la tua chiamata per scaricare un file

        if x == "0":
            break  # chiudi la connessione


def sendOsInfo(clientSocket):  # funzione che invia informazioni di sistema
    pack = "Architecture: " + platform.architecture()[
        0] + "\nMacchine: " + platform.machine() + "\nSystem name: " + platform.system()
    pack = pack + "\nOperating system release: " + platform.release() + "\nOperating system version: " + \
           platform.version() + "\nNode: " + platform.node() + "\nPlatform: " + platform.platform() + "\nProcessor: " + platform.processor()
    clientSocket.send(pack.encode())


def StartConnection():  # apre la connessione con il server
    serverName = 'localhost'
    serverPort = 12001
    clientSocket = socket(AF_INET, SOCK_STREAM)

    # aggiungere loop e controlli
    while True:
        try:
            clientSocket.connect((serverName, serverPort))
            break
        except:
            print("Server down")

        time.sleep(5)

    return clientSocket



def StopConnection(clientSocket):  # chiude la connessione con il server
    modifiedSentence = clientSocket.recv(1024)
    print('From Server:', modifiedSentence.decode())
    clientSocket.close()


if __name__ == '__main__':
    main()

# probabilmente si puo risolvere il problema dei pacchetti alternando sempre .send e . recv
# implementare error 404

# !non scrivere codice qui sotto!

