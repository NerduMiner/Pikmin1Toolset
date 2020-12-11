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

class BaseShape():
    def getIniFile(self, f):
        origin = f.tell()
        f.seek(-4,2) # move 4 bytes away from end 
        test = f.read() # read the rest of the file 
        f.seek(origin)
        if not test.decode("shift-jis").find("}") == -1:
            print("INI FILE DETECTED")
            return True
        return False
    
    def isolateINISections(f):
        fContents = []
        fContentType = []
        sectionRead = False
        sectionOpened = 0
        sectionClosed = 0
        for line in f:
            descriptor = CmdStream.getToken(line, 0)
            
            if not (line and line.strip()): # if line is white space
                continue # go to next iteration
            
            if not line.find("{") == -1:
                fContentType.append(CmdStream.getToken(line, 0) + "\n")
                sectionOpened = sectionOpened + 1
                sectionRead = True
            
            if not line.find("}") == -1:
                fContents.append(CmdStream.getToken(line, 0) + "\n")
                sectionClosed = sectionClosed + 1
                
                sectionRead = False
            
            if sectionRead: # if section has been found
                fContents.append(line) # append that line to the array
            
        if sectionOpened == sectionClosed:
            print(str(sectionOpened) + " INI sections detected") # make sure we confirmed amount of sections
            return fContents, fContentType
        return fContents, fContentType
    
    def importIni(filename, folder):
        with CmdStream.openFileInFolder(filename, folder, "r+") as f:
            fContents, fContentType = BaseShape.isolateINISections(f)
            if fContentType is not None:
                #print(fContentType)
                for i in range(len(fContentType)):
                    #print("CONTENT TYPE = " + str(fContentType[i]) + "\n")
                    if not fContentType[i].find("collinfo\n") == -1:
                        #print("COLLINFO!!")
                        ObjCollInfo.loadini(fContents)

                    if not fContentType[i].find("lightgroup\n") == -1:
                        #print("LIGHT GROUP!!")
                        LightGroup.loadini(fContents)

                    if not fContentType[i].find("routes\n") or fContentType[i].find("point\n") or fContentType[i].find("link\n") == -1:
                       # print("ROUTES!!")
                       pass
                    else:
                        print("ERR, UNKNOWN SECTION DETECTED")
                        return
            collect()

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
def AS_OpenFileInFolder(fileName, dirName, mode):
    # Create the directory if it hadn't been created already
    if not os.path.isdir(dirName):
        os.makedirs(dirName)

    if not dirName.endswith("/"):
        dirName += "/"

    end_filename = dirName + Path(fileName).name    
    return open(end_filename, mode)

