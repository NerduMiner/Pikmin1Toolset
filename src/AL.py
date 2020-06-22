import os
from gc import collect
from pathlib import Path
from struct import pack, unpack

# AL | AMRBOSIA LIBRARY

# Writing to a .obj file
class ObjFile():
    def __init__(self, f):
        self.fhandle = f

    def close(self):
        self.fhandle.close()

    def add_comment(self, comment):
        self.fhandle.write(f"# {comment}\n")

    def add_U32Trio(self, identifier, i1, i2, i3):
        self.fhandle.write(f"{identifier} {i1} {i2} {i3}\n")

    def add_F32Trio(self, identifier, f1, f2, f3):
        self.fhandle.write(f"{identifier} {f1} {f2} {f3}\n")

    def add_F32Duo(self, identifier, f1, f2):
        self.fhandle.write(f"{identifier} {f1} {f2}\n")

# Returns specified token in file
def GetToken(line, index):
    # Checks if the line is just whitespace
    splitLine = line.split()
    if (len(line) == 0 or len(splitLine) == 0):
        return ""

    # Check if the index goes under or above allowed indices
    if index > len(splitLine) - 1 or index < 0:
        return ""
    
    return splitLine[index]

# Returns file handle to the opened file
def OpenFileInFolder(fileName, dirName, mode):
    # Create the directory if it hadn't been created already
    if not os.path.isdir(dirName):
        os.makedirs(dirName)

    if not dirName.endswith("/"):
        dirName += "/"

    end_filename = dirName + Path(fileName).name    
    return open(end_filename, mode)

