import sys
import struct
import os
import io
from yoshiStuf import *
from ambroStuf import *
from gx import VertexDescriptor, VTXFMT, VTX

# Base provided by Yoshi2(RenolY2)
# Work done by NerduMiner, Ambrosia
def divSections(g, ini):
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
			inifile = f.read()
			ini.write(inifile.decode("shift-jis"))
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
	if len(sys.argv[1]) == 0:
		print("Usage: drag and drop mod file onto program")
	else:
		opcodes = [0x98,0x90,0xA0]
		skipdiff = 0
		ini = open(sys.argv[1]+".ini", "w+")
		with open(sys.argv[1], "rb") as f:
			mod_sections = divSections(f, ini)
			
		obj = open("output.obj", "w+")

		#First we're gonna get them sweet sweet verticies
		vertices = mod_sections[0x10][1]
		vertexNum = vertices.readInt32()
		print(str(vertexNum)+" vertices found.")

		#skip padding
		vertices.fhandle.read(0x14)
		for x in range(vertexNum):
			obj.write("v "+str(vertices.readFloat())+" "+str(vertices.readFloat())+" "+str(vertices.readFloat())+"\n")

		#Next, we will get the vertex normals
		normals = mod_sections[0x11][1]
		normalNum = normals.readInt32()
		print(normalNum,"vertex normals found.")
		
		#skip padding
		normals.fhandle.read(0x14)
		for x in range(normalNum):
			obj.write("vn "+str(normals.readFloat())+" "+str(normals.readFloat())+" "+str(normals.readFloat())+"\n")

		try:
			#now it is time for texture extracting
			textures = mod_sections[0x20][1]
			texNum = textures.readInt32()
			#t.write(struct.pack(">i", texNum))
			print(str(texNum)+" textures found")
			#skip padding
			textures.fhandle.read(0x14)
			for i in range(texNum):
				texFile = open("txe"+str(i)+".txe", "wb")
				width = textures.readUInt16()
				texFile.write(struct.pack(">H", width))
				height = textures.readUInt16()
				texFile.write(struct.pack(">H", height))
				unk = textures.readUInt16()
				texFile.write(struct.pack(">H", unk))
				format = textures.readUInt16()
				texFile.write(struct.pack(">H", format))
				unk2 = textures.readUInt32()
				texFile.write(struct.pack(">I", unk))
				print("txe",i,"data: W/H:",width,height,"format:",format)
				#textures.skipPadding()
				fpos = textures.fhandle.tell()+0x8
				if fpos % 0x20 == 0:
					continue
				skipto = (fpos - (fpos % 0x20)) + 0x20 
				skipdiff = skipto - textures.fhandle.tell() - 0x8
				textures.fhandle.read(skipdiff)
				print("skipped",skipdiff,"bytes of padding")
				for x in range(skipdiff):
					texFile.write(struct.pack("x"))
				texdata = textures.fhandle.read(calcSize(width,height,format))
				texFile.write(texdata)
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
			print(vcd)
			mtxgroupcnt = stream.readInt32()
			print(mtxgroupcnt)

			obj.write("o mesh"+str(batchNum)+"\n")

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
								obj.write("# 0x98\n")
							elif opcode == 0xA0:
								obj.write("# 0xA0\n")

							cPoly = triConv(cPoly, opcode)

							for poly in cPoly:
								obj.write("f "+str(poly[0])+" "+str(poly[1])+" "+str(poly[2])+"\n")
						elif opcode == 0x00:
							pass
						else:
							raise RuntimeError("unkown opcode "+opcode)
					assert stream.fhandle.tell() == endDsplist

					stream.fhandle.seek(dspStart + dspsize)
	obj.write("##" + texNum)
	BaseShape.importIni(ini)
