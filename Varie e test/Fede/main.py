import platform


print("Architecture: ", platform.architecture()[0])

print("Macchine: ", platform.machine())

print("System name: ", platform.system())

print("Operating system release: ", platform.release())

print("Operating system version: ", platform.version())

print("\nNode: ", platform.node())

print("\nPlatform: ", platform.platform())

print("\nProcessor: ", platform.processor())


#psutil.virtual_memory().total  # total physical memory in Bytes
'''x="c:\home\dir\ciao.txt"
k = x.split("\\")
x = k[1]

for n in k:
    x = n
print(x)'''
def main():
    br = input()
    print(br)
    RicercaFile(br,0)



#deprecata
import os
def RicercaFile(stri, clientSocket):
    rett = ""
    for cartella, sottocartella, files in os.walk(os.getcwd()):
        for file in files:
            if file.find(stri):
                #print(cartella + "\\" + file)
                rett = rett + cartella + "\\" + file + "\n"

    #clientSocket.send(rett.encode())
    print("il file è " + rett)
def DownloadFile(stri: str):

    local = os.walk(os.getcwd())
    pathar = stri.split("\\")
    gufo = ""
    for pat in pathar:
        print("pat = " + pat)
        for cartella in local:
            print("cartella = " + cartella[0])
            if cartella[0]==pat:
                local=cartella
                gufo = local[5]
                print(gufo)
                break
    print(gufo)

if __name__ == '__main__':
    main()
"""

import os
#prende nomi di tutti i file e le cartelle
#for cartella, sottocartelle, files in os.walk(os.getcwd()):
#    print(f"Ci troviamo nella cartella: '{cartella}'")
#    print(f"Le sottocartelle presenti sono: '{sottocartelle}'")
#    print(f"I files presenti sono: {files}")
#    print()

#prende nomi di tutti i file e le cartelle che finiscono con .py
for cartella, sottocartelle, files in os.walk("/"):
    #print(f"Ci troviamo nella cartella: '{cartella}'")
    #print(f"Le sottocartelle presenti sono: '{sottocartelle}'")
    for file in files:
        if file.__contains__("password.txt"):
            print(file)
            print(cartella + "\\" + file)
            g = cartella + "\\" + file
            #f = open(g,"r")
            #print(f.readlines())
            #f.close()

            #f = open(g , "r")

       #     while True:
        #        line = f.readline()
         #       if not line:
          #          break
          #      print(line)
            #f.close()
    #print()

#dir "\*termine da cercare*.*" /a /s
# Ricerca file Windows
"""

