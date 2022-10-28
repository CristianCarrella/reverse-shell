from socket import *

#flag da rivedere
windowsFlag = 0 # 0 per unix 1 per windows

def main():
    while True:
        try:
            connectionSocket = StartConnection() #apriamo connessione e inizializziamo

            while True: #funzione per menu loop fin quando non si inserisce zero
                x = MenuOperativo()
                InviaSelezioneMenu(x, connectionSocket)
                if x == "0":
                    break
                RiceviDaClient(x, connectionSocket) #funzione per ricevere da client

            StopConnection(connectionSocket) #chiude la connessione e termina
        except:
            print("errore Riavvio in corso")
            connectionSocket.close()
            break


def SalvaSuFile(str): #da usare da tutti per salvare i dati?
    f = open("dati.txt", "a") #forse dovremmo resettare il file a ogni avvio?
    f.write(str)
    f.close()


def RiceviDaClient(x, connectionSocket): #funzione di ritorno dopo menù
    if x == "1": #caso rirevi info OS
        d = connectionSocket.recv(1024).decode()
        SalvaSuFile(d) #salviamo i dati su file

        if d.find("Windows") != -1: #settiamo il flag
            global windowsFlag
            windowsFlag = 1
            print("si") #problemi con i flag? usiamo global?

    elif x == "2":
        print("gestire la shell")
        #inserisci funzione

    elif x == "3":
        print("fare una ricerca")
        #inserisci funzione

    elif x == "4":
        print("scaricare un file")
        #inserisci funzione


def MenuOperativo(): #funzione per menu (completa)

    # aggiungere controlli nel caso
    while True:
        x = 0
        print("ci troviamo su " + ("Windows" if windowsFlag else "Unix"))
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
            return x
        else:
            x = 0


def InviaSelezioneMenu(x, connectionSocket): #funzione per menu (completa)
    connectionSocket.send(x.encode())
    print(connectionSocket.recv(4).decode())


def StartConnection(): #funzione di connessione (da controllare)
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


def StopConnection(connectionSocket): #funzione di fine connesssione
    print('stopping the connection')
    if connectionSocket:
        connectionSocket.send(("end").encode())
        print("End")
        connectionSocket.close()


if __name__ == '__main__':
    main()

# !non scrivere codice qui sotto!