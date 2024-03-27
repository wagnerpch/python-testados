import os

filesName = []
pathToDirectory = r'C:\'
txtFileName = "lista_arquivos.txt"

def listFiles(directorySystem):
    for source, directories, files in os.walk(directorySystem):
        for file in files:
            filesName.append(os.path.join(source, file))

listFiles(pathToDirectory)

with open(txtFileName, "w") as file:
    for name in filesName:
        file.write(name + "\n")