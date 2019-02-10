#obj2mod time
import struct
import sys
import os
import datetime
from array import array
#Once we have edited or made a new obj, it's time to import
#This is as simple as creating new sections of a .mod file
#and using ModPacker to put everything together
faceNum = 0
vertexNum = 0
normNum = 0
array = []
fooce = []
norm = []
facedump = open("facedump.txt", "w")
with open(sys.argv[1], "r") as obj:
    for line in obj:
        if ('v') in line:
            #print(line)
            line = line[1:]
            array.append([float(x) for x in line.split()])
            #print(array)
            vertexNum += 1
        if ('#') in line:
            facedump.write(line)
            line = line[1:]
        if ('f') in line:
            #print(line)
            facedump.write(line)
            line = line[1:]
            fooce.append([int(x) for x in line.split()])
            #print(fooce)
            faceNum += 1
        if ('vn') in line:
            line = line[1:]
            norm.append([int(x) for x in line.split()])
            normNum += 1
    print(str(vertexNum) + " vertices found.")
    print(str(faceNum) + " faces found.")
facedump.close()
with open("out0x00.bin", "wb") as header:
    for x in range(24):
        header.write(struct.pack('x'))
    now = datetime.datetime.now()
    header.write(struct.pack(">H", now.year))
    header.write(struct.pack(">B", now.month))
    header.write(struct.pack(">B", now.day))
    header.write(struct.pack(">I", now.hour+now.minute+now.second))
    for x in range(24):
        header.write(struct.pack('x'))
with open("out0x10.bin", "wb") as vert:
    #0x10 starts with an identifier for how many vertices there are
    vertDef = struct.pack('>i', vertexNum)
    vert.write(vertDef)
    #0x20 alignment is practiced so we have to add 20 bytes of padding
    for x in range(20):
        vert.write(struct.pack('x'))
    #Now we can actually put in our data
    for x in range(vertexNum):
        for y in range(3):
            vertex = array[x][y]
            vertDef = struct.pack('>f', float(vertex))
            vert.write(vertDef)
print("Vertex data added successfully")
with open("out0x11.bin", "wb") as normal:
    #Add amount of normal vertices
    normal.write(struct.pack('>i', normNum))
    for x in range(20):
        normal.write(struct.pack('x'))
    for x in range(normNum):
        for y in range(3):
            normie = norm[x][y]
            normDef = struct.pack('>f', float(normie))
            normal.write(normDef)
print("Normal data added successfully")
#with open("out0x20.bin", "wb") as textures:
batchCnt = 0
batchNum = []
opcodes = []
# We need to figure out how many batches we have and how many faces
# are in each batch
with open("facedump.txt", "r") as faceRead:
    for line in faceRead:
        if ('#') in line:
            if ("0x98") in line:
                opcode = 0x98
                if batchCnt == 0:
                    continue
                else:
                    opcodes.append(0x98)
                    batchNum.append(batchCnt)
                    batchCnt = 0
            elif ("0xA0") in line:
                opcode = 0xA0
                if batchCnt == 0:
                    continue
                else:
                    opcodes.append(0xA0)
                    batchNum.append(batchCnt)
                    batchCnt = 0
        else:
            batchCnt += 1
with open("out0x50.bin", "wb") as face:
    print("batchNum",len(batchNum),"# of opcodes",len(opcodes))
    face.write(struct.pack(">i", len(batchNum)))
    # correctly pad out the section
    faceoutput = "out0x50.bin"
    size = face.tell()+8
    print(size,"bytes before padding")
    if size % 32 != 0:
        padNum = 32 - (size % 32)
    else:
        padNum = 0
    padding = [0x0 for x in range(padNum)]
    face.write(bytearray(padding))
    print(padNum,"bytes padded")
    #There's some extra things that we need to add
    face.write(struct.pack(">i", 0xDEAD))#unk1
    face.write(struct.pack(">i", 0xBEEF))#vcd
    face.write(struct.pack(">i", 0xDEAD))#matrixgroupcount
    face.write(struct.pack(">i", 0xBEEF))#unkcount
    face.write(struct.pack(">H", 0xDE))#vals
    face.write(struct.pack(">I", 0xADBE))#unkown2
    face.write(struct.pack(">I", 0xEFDE))#command count
    face.write(struct.pack(">I", 0xADBE))#disp size
    size = face.tell()+8
    print(size,"bytes before padding")
    if size % 32 != 0:
        padNum = 32 - (size % 32)
    else:
        padNum = 0
    padding = [0x0 for x in range(padNum)]
    face.write(bytearray(padding))
    print(padNum,"bytes padded")
    #This is where we finally add in the face data
    for x in range(len(batchNum)):
        face.write(struct.pack(">B", opcodes[x]))
        y = 0
        for y in range(batchNum[y]):
            face.write(struct.pack(">H", fooce[y][0]))
            face.write(struct.pack(">H", fooce[y][1]))
            face.write(struct.pack(">H", fooce[y][2]))
    #Finally we must pad out to the next multiple of 32 bytes
    faceoutput = "out0x50.bin"
    #Add 8 to size because of section header
    size = face.tell()+8
    print(size,"bytes before padding")
    if size % 32 != 0:
        padNum = 32 - (size % 32)
    else:
        padNum = 0
    padding = [0x0 for x in range(padNum)]
    face.write(bytearray(padding))
    print(padNum,"bytes padded")
print("Face data added completely")
with open("out0xFFFF") as EOF:
    for x in range(24):
        EOF.write(struct.pack('x'))
print("EOF Chunk added successfully")
    #P S E U D O C O D E
    #create header data
    #face.write(headerData)
    #for x in range(faceNum):
    #   We use 4 because the format is as follows:
    #   face, uv, vertex-color, normals
    #   for y in range(3):
    #       face = fooce[x][y]
    #       faceDef = struct.pack('>H', face)
    #       face.write(faceDef)
