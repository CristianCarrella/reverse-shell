# Funzione di ricerca di un file dalla working directory LATO SERVER
    # SO: 'w' per windows, 'u' per unix
  
def searchFile(SO, connectionSocket):
        print(connectionSocket.recv(1024).decode())
        string = input("String: ")
        if(SO == "w"):
            cmd = "dir \"" + string + "\" /a /s"
        else:
            cmd = "find -name " + string
        connectionSocket.send(cmd.encode())
        print("Ricerca...")
        pSize = int(connectionSocket.recv(1024).decode())
        mex = "Server pronto a ricevere l'output"
        connectionSocket.send(mex.encode())
        output = str(connectionSocket.recv(pSize).decode())
        print(output)
        return output
