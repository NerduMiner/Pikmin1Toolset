import os
class CmdStream():    
    def getToken(line, getTokenIndex):
        if not (line and line.strip()): # if whitespace
            return ""
        #if hasComments:
         #   line.split("//", 1)
        try:
            if line:
                return line.split()[getTokenIndex]
        except IndexError:
            pass

class ObjCollInfo():
    def loadini(fContents):
        for line in fContents:
            if not line.find("{") == -1: # if closed bracket
                print("opening bracket found!")
                print("name of collinfo part : " + CmdStream.getToken(line, -1))

            if not line.find("id") == -1:
                print("id : " + CmdStream.getToken(line, 1))

            if not line.find("code") == -1:
                print("code : " + CmdStream.getToken(line, 1))

            if not line.find("type") == -1:
                print("type : " + CmdStream.getToken (line,1))

            if not line.find("platform") == -1:
                print("platform : " + CmdStream.getToken(line, 1))

            if not line.find("radius") == -1:
                print("radius : " + CmdStream.getToken(line, 1))

            if not line.find("getminy") == -1:
                print("get minimum y : " + CmdStream.getToken(line, 1))

            if not line.find("collinfo") == -1:
                print("REPEATING COLLINFO FUNC!!!")
                
            if not line.find("}") == -1: # if closed bracket
                print("closed bracket found!\n\n")
                return

class LightGroup():
    def loadini(fContents):
        for line in fContents:
            if not line.find("{") == -1: # if closed bracket
                print("opening bracket found!")
                print("name of lightgroup part : " + CmdStream.getToken(line, -1))

            if not line.find("type") == -1:
                print("type : " + CmdStream.getToken (line,1))

            if not line.find("flags") == -1:
                print("flags : " + CmdStream.getToken(line, 1))

            if not line.find("colour") == -1:
                print("colour : " + CmdStream.getToken(line, 1) + CmdStream.getToken(line, 2) + CmdStream.getToken(line, 3) + CmdStream.getToken(line, 4))

            if not line.find("texture") == -1:
                print("texture name : " + CmdStream.getToken(line, 1))

            if not line.find("material") == -1:
                print("material name : " + CmdStream.getToken(line, 1))

            if not line.find("lightflare") == -1:
                print("lightflare detected! \n")

            if not line.find("size") == -1:
                print("size of lightflare : " + CmdStream.getToken(line, 1))

            if not line.find("pos") == -1:
                print("position of lightflare : " + CmdStream.getToken(line, 1) + CmdStream.getToken(line, 2) + CmdStream.getToken(line, 3))
                
            if not line.find("}") == -1: # if closed bracket
                print("closed bracket found!\n\n")
                return

class BaseShape():
    def isolateINISections(f):
        fContents = []
        fContentType = []
        sectionRead = False
        sectionOpened = 0
        sectionClosed = 0
        for line in f: # while (!Cmdstream::endofcmds(v18) && !Cmdstream::endofsection(v18))
            descriptor = CmdStream.getToken(line, 0) #CmdStream::isToken

            if not (line and line.strip()): # if line is white space 
                continue # just go to the next iteration

            if not line.find("{") == -1: # if open bracket
                fContentType.append(CmdStream.getToken(line, 0) + "\n")
                sectionOpened = sectionOpened + 1
                sectionRead = True

            if not line.find("}") == -1: # if closed bracket
                fContents.append(CmdStream.getToken(line, 0) + "\n") # append that line to the array
                sectionClosed = sectionClosed + 1
                
                sectionRead = False

            if sectionRead: # if section has been found
                fContents.append(line) # append that line to the array

        if sectionOpened == sectionClosed:
            print(str(sectionOpened) + " sections detected") # make sure we have confirmed amount of sections
            #print("section content types are:\n"+"".join(fContentType))
            return fContents, fContentType
        return fContents, fContentType# return the sections
    
    def importIni(f):
        print("PRINTING INI INFO... \n \n \n")
        fContents, fContentType = BaseShape.isolateINISections(f)
        for i in range(len(fContentType)):
            #print("CONTENT TYPE = " + str(fContentType[i]) + "\n")
            if not fContentType[i].find("collinfo\n") == -1:
                print("COLLINFO!!")
                ObjCollInfo.loadini(fContents)
            if not fContentType[i].find("lightgroup\n") == -1:
                print("LIGHT GROUP!!")
                LightGroup.loadini(fContents)
            if not fContentType[i].find("routes") == -1:
                print("ROUTES!!")



