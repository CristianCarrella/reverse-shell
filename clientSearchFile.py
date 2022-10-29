# Funzione di ricerca di un file dalla working directory LATO CLIENT
import subprocess


def searchCmd(clientSocket):
    mex = "Client pronto a ricevere la stringa"
    clientSocket.send(mex.encode())
    cmd = clientSocket.recv(1024).decode()
    print(cmd)
    try:
        output = subprocess.check_output(cmd, shell = True).decode("utf-8", "ignore")
    except:
        output = "Errore: nessun file trovato"
    pSize = str(output.__sizeof__())
    clientSocket.send(pSize.encode())
    print(clientSocket.recv(1024).decode())
    clientSocket.send(output.encode())

    #Aggiungere controllo se inserisco stringa vuota o no?(restituisce tutto)#
    #
    #
    #
