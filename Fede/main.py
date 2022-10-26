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

