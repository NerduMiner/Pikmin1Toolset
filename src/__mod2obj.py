'''
The Zen of Python, by Tim Peters

Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!
'''

import sys
import struct
import os
import io
from yoshiStuf import *
from gx import VertexDescriptor, VTXFMT, VTX

# Base provided by Yoshi2(RenolY2)
# Work done by NerduMiner, Ambrosia
from ambroStuf import *
def divSections(g):
        sections = {}
        result = None
        while True:
                start = g.tell() # assign start of section
                if 0xFFFF not in sections:
                        #unpack into 2 unsigned integers, retreieve ID and length
                        meta = g.read(8)
                        if len(meta) == 8: # if the length of metadata (g.read(8)) == 8 then..
                                ID, length = struct.unpack(">II", meta)
                                #print("opcode:",struct.pack('>I',ID),"Length:",length,"bytes \n")
                                data = g.read(length)
                        
                                result = ID, length, data
                                if result is not None:
                                        ID, length, data = result
                                        sections[ID] = (length, bStream(io.BytesIO(data)), start)
                                else:
                                        break
                        #if we have a proper header, put this all into sections
                        
                else:
                        if BaseShape.getIniFile(g):
                                ini = open(sys.argv[1]+".ini", "r+")
                                inifile = f.read()
                                ini.write(inifile.decode("shift-jis"))
                                BaseShape.importIni(ini)
                        break
        return sections

def triConv(poly, opc):
        if len(poly) == 3:
                return [poly]
                
        newTri = []
        
        if (opc == 0x98):
                n = 2
                for x in range(len(poly)-2):
                        Tri = []
                        isEven = (n%2) == 0
                        #if n == 2:
                        #1. append first poly
                        #2. append last poly since n is even
                        #3. append second poly since n is even
                        Tri.append(poly[n-2])
                        Tri.append((poly[n] if isEven else poly[n-1]))
                        Tri.append((poly[n-1] if isEven else poly[n]))
                        if (Tri[0] != Tri[1] and Tri[1] != Tri[2] and Tri[2] != Tri[0]):
                                newTri.append(Tri)
                        n += 1
        
        if (opc == 0xA0):
                for x in range(1, len(poly)-1):
                        Tri = []
                        #append tris second, last, first
                        Tri.append(poly[x])
                        Tri.append(poly[x+1])
                        Tri.append(poly[0])
                        if (Tri[0] != Tri[1] and Tri[1] != Tri[2] and Tri[2] != Tri[0]):
                                newTri.append(Tri)
        
        return newTri

def countOnes(n, max=32):
        x = 0
        for i in range(max):
                if (n >> i) & 1 == 1:
                        x += 1
        return x

def calcSize(w, h, format):
        if format in (0,2,6):
                return w*h*2
        elif format == 1:
                return w*h//2
        elif format == 3:
                return w*h//2
        elif format in (4,5,8):
                return w*h
        elif format == 7:
                return w*h*4
        else:
                raise RuntimeError("unkown texture format: ",format)

def __enter__(self):
        return self

if __name__ == "__main__":
        try:
                var = sys.argv[1]
        except IndexError:
                print(".mod to .obj")
                print("USAGE: drag and drop mod file onto program\n")
                print("Main programmers, NerduMiner, Ambrosia")
                print("Special thanks to RenolY2 AKA Yoshi2 for the face reading base.")
                
        else:
                opcodes = [0x98,0x90,0xA0]
                skipdiff = 0
                with open(sys.argv[1], "rb") as f:
                        mod_sections = divSections(f)
                        
                obj = open("output.obj", "w+")
                objWrite = obj.write

                #First we're gonna get them sweet sweet verticies
                vertices = mod_sections[0x10][1]
                vertexNum = vertices.readInt32()
                print(str(vertexNum)+" vertices found.")

                #skip padding
                vertices.fhandle.read(0x14)
                for x in range(vertexNum):
                        objWrite("v "+str(vertices.readFloat())+" "+str(vertices.readFloat())+" "+str(vertices.readFloat())+"\n")

                #Next, we will get the vertex normals
                normals = mod_sections[0x11][1]
                normalNum = normals.readInt32()
                print(normalNum,"vertex normals found.")
                
                #skip padding
                normals.fhandle.read(0x14)
                for x in range(normalNum):
                        objWrite("vn "+str(normals.readFloat())+" "+str(normals.readFloat())+" "+str(normals.readFloat())+"\n")

                try:
                        #now it is time for texture extracting
                        textures = mod_sections[0x20][1]
                        texNum = textures.readInt32()
                        print(str(texNum)+" textures found \n")
                        #skip padding
                        textures.fhandle.read(0x14)
                        for i in range(texNum):
                                texFile = open("txe"+str(i)+".txe", "wb")
                                #cache write function
                                texWrite = texFile.write
                                width = textures.readUInt16() # get vars
                                height = textures.readUInt16()
                                unk = textures.readUInt16()
                                format = textures.readUInt16()
                                unk2 = textures.readUInt32()
                                
                                texWrite(struct.pack(">H", format)) # write vars
                                texWrite(struct.pack(">H", width))
                                texWrite(struct.pack(">H", height))
                                texWrite(struct.pack(">H", unk))
                                texWrite(struct.pack(">I", unk))
                                print("txe",i,"data: W/H:",width,height,"format:",format, "\n")
                                fpos = textures.fhandle.tell()+0x8
                                if fpos % 0x20 == 0:
                                        continue
                                skipto = (fpos - (fpos % 0x20)) + 0x20 
                                skipdiff = skipto - textures.fhandle.tell() - 0x8
                                textures.fhandle.read(skipdiff)
                                print("skipped",skipdiff,"bytes of padding")
                                
                                for x in range(skipdiff):
                                        texWrite(struct.pack("x"))

                                        
                                texdata = textures.fhandle.read(calcSize(width,height,format))
                                texWrite(texdata)
                except KeyError as err:
                        print("No textures found, skipping")
                #Next we do the faces
                stream, triStart = mod_sections[0x50][1], mod_sections[0x50][2]
                print("vertices start at", hex(triStart))
                batchCount = stream.readInt32()
                stream.skipPadding()

                for batchNum in range(batchCount):
                        unkown1 = stream.readInt32()
                        vcd = VertexDescriptor()
                        vcd.from_pikmin1(stream.readInt32(), hasNormals=0x11 in mod_sections)
                        mtxgroupcnt = stream.readInt32()
                        objWrite("o mesh"+str(batchNum)+"\n")

                        for mtxgroupnum in range(mtxgroupcnt):
                                unkcnt = stream.readInt32()
                                vals = []
                                for i in range(unkcnt):
                                        vals.append(stream.readUInt16())

                                dsplstcnt = stream.readInt32()

                                for dsplstnum in range(dsplstcnt):
                                        unkown1 = stream.readUInt32()
                                        cmdcnt = stream.readUInt32()
                                        dspsize = stream.readUInt32()

                                        stream.skipPadding()

                                        dspStart = stream.fhandle.tell()

                                        dispdata = stream.fhandle.read(dspsize)
                                        stream.fhandle.seek(dspStart)
                                        endDsplist = dspStart + dspsize

                                        while stream.fhandle.tell() < endDsplist:
                                                opcode = stream.readUInt8()

                                                if opcode in (0x98, 0xA0):
                                                        vCnt = stream.readUInt16()
                                                        cPoly = []
                                                        for x in range(vCnt):
                                                                posIdx = None
                                                                for attr, format in vcd.active_attributes():
                                                                        if attr == VTX.Position:
                                                                                posIdx = stream.readUInt16()+1
                                                                        elif format is None:
                                                                                stream.readUInt8()
                                                                        elif format == VTXFMT.INDEX16:
                                                                                stream.readUInt16()
                                                                        else:
                                                                                raise RuntimeError("format error")
                                                                #Make sure posIdx isn't empty
                                                                assert posIdx is not None
                                                                cPoly.append(posIdx)
                                                                
                                                        if opcode == 0x98:
                                                                objWrite("# 0x98\n")
                                                        elif opcode == 0xA0:
                                                                objWrite("# 0xA0\n")

                                                        cPoly = triConv(cPoly, opcode)

                                                        for poly in cPoly:
                                                                objWrite("f "+str(poly[0])+" "+str(poly[1])+" "+str(poly[2])+"\n")
                                                elif opcode == 0x00:
                                                        pass
                                                else:
                                                        raise RuntimeError("unkown opcode "+opcode)
                                        assert stream.fhandle.tell() == endDsplist

                                        stream.fhandle.seek(dspStart + dspsize)
                try:
                        objWrite("##" + str(texNum))
                except NameError:
                        print("No textures to reference in obj")

