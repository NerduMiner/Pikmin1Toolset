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

#sys.argv[1] == OBJ FILE
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

#sys.argv[2] == MOD FILE?
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
    outputMod.write(struct.pack('>I', modSection[0x00][0]))
    head = modSection[0x00][1].packRead(modSection[0x00][0])
    outputMod.write()

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
    #You'd have to be very stupid to get this code to run
    outputMod.write(struct.pack('>I', 0x00000010))
    outputMod.write(struct.pack('>I', modSection[0x10][0]))
    ver = modSection[0x10][1].packRead(modSection[0x10][0])
    outputMod.write()
print("Vertex data added successfully")

if 0x13 in modSection:
    #Per Mesh Textures Hue Modifiers
    outputMod.write(struct.pack('>I', 0x00000013))
    outputMod.write(struct.pack('>I', modSection[0x13][0]))
    mesh = modSection[0x13][1].packRead(modSection[0x13][0])
    outputMod.write(mesh)
    write_pad32(outputMod)
print("Per Mesh Textures Hue Modifiers added successfully")

#with open("out0x11.bin", "wb+") as normal:
if 0x11 in sections and 0x11 in modSection:
    normal = []
    #Add amount of normal vertices
    normal.append(struct.pack('>i', normNum))
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
    outputMod.write(struct.pack('>I', modSection[0x11][0]))
    normi = modSection[0x11][1].packRead(modSection[0x11][0])
    for byte in normi:
        outputMod.write(byte)
    write_pad32(outputMod)
print("Normal data added successfully")

if 0x18 in modSection:
    #UV Mapping
    outputMod.write(struct.pack('>I', 0x00000018))
    outputMod.write(struct.pack('>I', modSection[0x18][0]))
    uv = modSection[0x18][1].packRead(modSection[0x18][0])
    for byte in uv:
        outputMod.write(byte)
    write_pad32(outputMod)
print("UV Mapping added successfully.")

if 0x19 in modSection:
    #Unk section 0x19
    outputMod.write(struct.pack('>I', 0x00000019))
    outputMod.write(struct.pack('>I', modSection[0x19][0]))
    unk19 = modSection[0x19][1].packRead(modSection[0x19][0])
    for byte in unk19:
        outputMod.write(byte)
    write_pad32(outputMod)
print("Unkown section 0x19 added successfully")

if 0x1A in modSection:
    #Unk section 0x1A
    outputMod.write(struct.pack('>I', 0x0000001A))
    outputMod.write(struct.pack('>I', modSection[0x1A][0]))
    unk1A = modSection[0x1A][1].packRead(modSection[0x1A][0])
    for byte in unk1A:
        outputMod.write(byte)
    write_pad32(outputMod)
print("Unkown section 0x1A added successfully")

#with open("out0x20.bin", "wb+") as textures:
if 0x20 in sections and 0x20 in modSection:
    textures = []
    textures.append(struct.pack('>i', texNum))
    #Add Padding
    for x in range(20):
        textures.append(struct.pack('x'))
    for x in range(texNum):
        txes = open(str("textures/txe"+str(x)+".txe"), 'rb')
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
    try:
        outputMod.write(struct.pack('>I', 0x00000020))
        outputMod.write(struct.pack('>I', modSection[0x20][0]))
        modSecB = modSection[0x20][1].packRead(modSection[0x20][0])
        outputMod.write(modSecB)
        write_pad32(outputMod)
    except KeyError:
        print("No textures associated, skipping")
print("Texture data added")


if 0x22 in modSection:
    #Mipmap Data Chunk
    outputMod.write(struct.pack('>I', 0x00000022))
    outputMod.write(struct.pack('>I', modSection[0x22][0]))
    mipB = modSection[0x22][1].packRead(modSection[0x22][0])
    for byte in mipB:
        outputMod.write(byte)
    write_pad32(outputMod)
print("Mipmap Data added successfully")

if 0x30 in modSection:
    #Mesh Color Definitions
    outputMod.write(struct.pack('>I', 0x00000030))
    outputMod.write(struct.pack('>I', modSection[0x30][0]))
    meshB = modSection[0x30][1].packRead(modSection[0x30][0])
    for byte in meshB:
        outputMod.write(byte)
    write_pad32(outputMod)
print("Mesh Color Definitions added successfully")

if 0x40 in modSection:
    #Unk Chunk 0x40
    outputMod.write(struct.pack('>I', 0x00000040))
    outputMod.write(struct.pack('>I', modSection[0x40][0]))
    unkB = modSection[0x40][1].packRead(modSection[0x40][0])
    for byte in unkB:
        outputMod.write(byte)
    write_pad32(outputMod)
print("Unk section 0x40 added successfully")

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
        for faces in fooce[x]:
            face.append(struct.pack(">H", faces))
    #Finally we must pad out to the next multiple of 32 bytes
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
    outputMod.write(struct.pack('>I', modSection[0x50][0]))
    faces = modSection[0x50][1].packRead(modSection[0x50][0])
    outputMod.write()
print("Face data added completely")


if 0x60 in modSection:
    #Unk Chunk 0x60
    outputMod.write(struct.pack('>I', 0x00000060))
    outputMod.write(struct.pack('>I', modSection[0x60][0]))
    unkBB = modSection[0x60][1].packRead(modSection[0x60][0])
    for byte in unkBB:
        outputMod.write(byte)
    write_pad32(outputMod)
print("unk section 0x60 added successfully")


if 0x80 in modSection:
    #Texture Palettes Chunk
    outputMod.write(struct.pack('>I', 0x00000080))
    outputMod.write(struct.pack('>I', modSection[0x80][0]))
    texB = modSection[0x80][1].packRead(modSection[0x80][0])
    for byte in texB:
        outputMod.write(byte)
    write_pad32(outputMod)
print("Texture Palettes added successfully")

if 0x100 in modSection:
    #Floor Collision Geometry
    outputMod.write(struct.pack('>I', 0x00000100))
    outputMod.write(struct.pack('>I', modSection[0x100][0]))
    floorB = modSection[0x100][1].packRead(modSection[0x100][0])
    for byte in floorB:
        outputMod.write(byte)
    write_pad32(outputMod)
print("Floor Collision Geometry added successfully")

if 0x110 in modSection:
    #MapMgr bounds + Coll Tris
    outputMod.write(struct.pack('>I', 0x00000110))
    outputMod.write(struct.pack('>I', modSection[0x110][0]))
    mapB = modSection[0x110][1].packRead(modSection[0x110][0])
    for byte in mapB:
        outputMod.write(byte)
    write_pad32(outputMod)
print("MapMgr Bounds + Coll Tris added successfully")

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
try:
    #sys.argv[3] as INI?
    with open(sys.argv[3], 'rb') as ini:
        outputModWrite = outputMod.write
        while True:
            try:
                char = struct.pack(">c", ini.read(1))
                print(char)
                outputModWrite(char)
            except Exception:
                print("done")
                break
except IndexError:
    print("No ini found, skipping")
print("ini writing finished")


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
