#obj2mod time
import struct
import sys
import os
import io
from yoshiStuf import *
from array import array
from datetime import datetime
#Once we have edited or made a new obj, it's time to import
#This is as simple as creating new sections of a .mod file
#and using ModPacker to put everything together
faceNum = 0
vertexNum = 0
normNum = 0
array = []
fooce = []
norm = []
sections = [0x00, 0xFFFF]
facedump = open("facedump.txt", "w+")
outputMod = open("output.mod", 'wb+')

def write_pad32(f): # IMPORTANT
    next_aligned_pos = (f.tell() + 0x1F) & ~0x1F

    f.write(b"\x00"*(next_aligned_pos - f.tell()))

def divSections(g):
    sections = {}
    result = None
    while True:
        #setup pointer in .mod file
        start = g.tell()
        if 0xFFFF not in sections:
            #read 8 bytes of data
            meta = g.read(8)
            #unpack into 2 unsigned integers, retreieve ID and length
            if len(meta) == 8:
                ID, length = struct.unpack(">II", meta)
                print("ID:",struct.pack('>I',ID),"Length:",length,"bytes")
                data = g.read(length)

                result = ID, length, data
            else:
                result = None
                #if we have a proper header, put this all into sections
            if result is not None:
                ID, length, data = result
                sections[ID] = (length, bStream(io.BytesIO(data)), start)
            else:
                break
        else:
            break
    return sections

with open(sys.argv[1], "r") as obj:
    for line in obj:
        if ('vn') in line:
            if 0x11 not in sections:
                sections.append(0x11)
            line = line[2:]
            norm.append([float(x) for x in line.split()])
            normNum += 1
        if ('v') in line:
            if 0x10 not in sections:
                sections.append(0x10)
            line = line[1:]
            array.append([float(x) for x in line.split()])
            #print(array)
            vertexNum += 1
        if ('##') in line:
            if 0x20 not in sections:
                sections.append(0x20)
            texNum = int(line[2:])
            print(texNum,"textures found")
        if ('#') in line:
            facedump.write(line)
            line = line[1:]
        if ('f') in line:
            if 0x50 not in sections:
                sections.append(0x50)
            #print(line)
            facedump.write(line)
            line = line[1:]
            fooce.append([int(x) for x in line.split()])
            #print(fooce)
            faceNum += 1
    print(str(vertexNum) + " vertices found.")
    print(str(faceNum) + " faces found.")
facedump.close()

with open(sys.argv[2], "rb") as f:
    modSection = divSections(f)

print(sections)
print(modSection)

#with open("out0x00.bin", "wb+") as header:
if 0x00 in sections and 0x00 in modSection:
    header = []
    for x in range(24):
        header.append(struct.pack('x'))
    time = datetime.now()
    header.append(struct.pack(">H", time.year))
    header.append(struct.pack(">B", time.month))
    header.append(struct.pack(">B", time.day))
    header.append(struct.pack(">I", time.hour+time.minute+time.second))
    for x in range(24):
        header.append(struct.pack('x'))
    outputMod.write(struct.pack('>I', 0x00000000))
    outputMod.write(struct.pack('>I', len(header)))
    headerD = []
    headerDataAppend = headerD.append
    outputModWrite = outputMod.write
    for data in header:
        headerDataAppend (data)
    for byte in headerD:
        outputModWrite (byte)
    write_pad32(outputMod)
    header = []
else:
    outputMod.write(struct.pack('>I', 0x00000000))
    outputMod.write(modSection[0x00][1])

#with open("out0x10.bin", "wb+") as vert:
if 0x10 in sections and 0x10 in modSection:
    vert = []
    #0x10 starts with an identifier for how many vertices there are
    vertDef = struct.pack('>i', vertexNum)
    vert.append(vertDef)
    #0x20 alignment is practiced so we have to add 20 bytes of padding
    for x in range(20):
        vert.append(struct.pack('x'))
    #Now we can actually put in our data
    for x in range(vertexNum):
        for y in range(3):
            vertex = array[x][y]
            vertDef = struct.pack('>f', float(vertex))
            vert.append(vertDef)
    outputMod.write(struct.pack('>I', 0x00000010))
    outputMod.write(struct.pack('>I', len(vert)))
    vertD = []
    vertDataAppend = vertD.append
    outputModWrite = outputMod.write
    for data in vert:
        vertDataAppend (data)
    for byte in vertD:
        outputModWrite (byte)
    write_pad32(outputMod)
    vert = []
else:
    outputMod.write(struct.pack('>I', 0x00000010))
    outputMod.write(modSection[0x10][0])
    outputMod.write(modSection[0x10][1])
print("Vertex data added successfully")

#with open("out0x11.bin", "wb+") as normal:
if 0x11 in sections and 0x11 in modSection:
    normal = []
    #Add amount of normal vertices
    normal.append(struct.pack('>i', normNum))
    for x in range(20):
        normal.append(struct.pack('x'))
    for x in range(normNum):
        for y in range(3):
            normie = norm[x][y]
            normDef = struct.pack('>f', float(normie))
            normal.append(normDef)
    outputMod.write(struct.pack('>I', 0x00000011))
    outputMod.write(struct.pack('>I', len(normal)))
    normalD = []
    normalDataAppend = normalD.append
    outputModWrite = outputMod.write
    for data in normal:
        normalDataAppend (data)
    for byte in normalD:
        outputModWrite (byte)
    write_pad32(outputMod)
    normal = []
else:
    outputMod.write(struct.pack('>I', 0x00000011))
    outputMod.write(modSection[0x11][0])
    outputMod.write(modSection[0x11][1])
print("Normal data added successfully")

#with open("out0x20.bin", "wb+") as textures:
if 0x20 in sections and 0x20 in modSection:
    textures = []
    textures.append(struct.pack('>i', texNum))
    #Add Padding
    for x in range(20):
        textures.append(struct.pack('x'))
    for x in range(texNum):
        txes = open(str("txe"+str(x)+".txe"), 'rb')
        textures.append(txes.read())
    outputMod.write(struct.pack('>I', 0x00000020))
    outputMod.write(struct.pack('>I', len(textures)))
    textureD = []
    textureDataAppend = textureD.append
    outputModWrite = outputMod.write
    for data in textures:
        textureDataAppend (data)
    for byte in textureD:
        outputModWrite (byte)
    write_pad32(outputMod)
    textures = []
else:
    outputMod.write(struct.pack('>I', 0x00000020))
    outputMod.write(modSection[0x20][0])
    outputMod.write(modSection[0x20][1])
print("Texture data added")

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
#with open("out0x50.bin", "wb") as face:
if 0x50 in sections and 0x50 in modSection:
    face = []
    print("batchNum",len(batchNum),"# of opcodes",len(opcodes))
    face.append(struct.pack(">i", len(batchNum)))
    # correctly pad out the section
    faceoutput = "out0x50.bin"
    size = len(face)+8
    print(size,"bytes before padding")
    if size % 32 != 0:
        padNum = 32 - (size % 32)
    else:
        padNum = 0
    padding = [0x0 for x in range(padNum)]
    face.append(bytearray(padding))
    print(padNum,"bytes padded")
    #There's some extra things that we need to add
    face.append(struct.pack(">i", 0xDEAD))#unk1
    face.append(struct.pack(">i", 0xBEEF))#vcd
    face.append(struct.pack(">i", 0xDEAD))#matrixgroupcount
    face.append(struct.pack(">i", 0xBEEF))#unkcount
    face.append(struct.pack(">H", 0xDE))#vals
    face.append(struct.pack(">I", 0xADBE))#unkown2
    face.append(struct.pack(">I", 0xEFDE))#command count
    face.append(struct.pack(">I", 0xADBE))#disp size
    size = len(face)+8
    print(size,"bytes before padding")
    if size % 32 != 0:
        padNum = 32 - (size % 32)
    else:
        padNum = 0
    padding = [0x0 for x in range(padNum)]
    face.append(bytearray(padding))
    print(padNum,"bytes padded")
    #This is where we finally add in the face data
    for x in range(len(batchNum)):
        face.append(struct.pack(">B", opcodes[x]))
        y = 0
        for y in range(batchNum[y]):
            face.append(struct.pack(">H", fooce[y][0]))
            face.append(struct.pack(">H", fooce[y][1]))
            face.append(struct.pack(">H", fooce[y][2]))
    #Finally we must pad out to the next multiple of 32 bytes
    faceoutput = "out0x50.bin"
    #Add 8 to size because of section header
    size = len(face)+8
    print(size,"bytes before padding")
    if size % 32 != 0:
        padNum = 32 - (size % 32)
    else:
        padNum = 0
    padding = [0x0 for x in range(padNum)]
    face.append(bytearray(padding))
    print(padNum,"bytes padded")
    outputMod.write(struct.pack('>I', 0x00000050))
    outputMod.write(struct.pack('>I', len(face)))
    faceD = []
    faceDataAppend = faceD.append
    outputModWrite = outputMod.write
    for data in face:
        faceDataAppend (data)
    for byte in faceD:
        outputModWrite (byte)
    write_pad32(outputMod)
    face = []
else:
    outputMod.write(struct.pack('>I', 0x00000050))
    outputMod.write(modSection[0x50][0])
    outputMod.write(modSection[0x50][1])
print("Face data added completely")

#with open("out0xFFFF", 'wb') as EOF:
if 0xFFFF in sections and 0xFFFF in modSection:
    EOF = []
    for x in range(24):
        EOF.append(struct.pack('x'))
    outputMod.write(struct.pack('>I', 0x0000FFFF))
    outputMod.write(struct.pack('>I', len(EOF)))
    EOFD = []
    EOFDataAppend = EOFD.append
    outputModWrite = outputMod.write
    for data in EOF:
        EOFDataAppend (data)
    for byte in EOFD:
        outputModWrite (byte)
    write_pad32(outputMod)
    EOF = []
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
