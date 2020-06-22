import YL
import AL
import struct
from gx import VertexDescriptor, VTXFMT, VTX
import io
import sys
import image_gc

# Returns all sections in the MOD file
def SplitModToSections(fileHandle):
    sections = {}

    # Loop until EOF
    while 0xFFFF not in sections:
        # Grab the Chunk's offset and metadata
        chunk_offset = fileHandle.tell()
        meta_data = fileHandle.read(8)

        # Grab the Chunk ID and the length of the Chunk via it's header
        chunk_id, chunk_len = struct.unpack(">II", meta_data)
        chunk_data = fileHandle.read(chunk_len)

        # Insert the chunk and a stream pointing to the chunk into the sections set
        sections[chunk_id] = [chunk_len, YL.bStream(chunk_data), chunk_offset]

    return sections

def ConvertToObjTriangle(poly, opcode):
    if len(poly) == 3:
        return [poly]
        
    '''
    | Opcode Cheat Sheet |
    POINTS == 0xB8
    LINES == 0xA8
    LINESTRIP == 0xB0
    TRIANGLES == 0x90
    TRIANGLESTRIP == 0x98
    TRIANGLEFAN == 0xA0
    QUADS == 0x80
    '''
    
    newTri = []
    
    if opcode == 0x98:
        n = 2
        for i in range(len(poly) - 2):
            isEven = n % 2 == 0
            attemptedTri = [poly[n - 2],
                            poly[n] if isEven else poly[n - 1], 
                            poly[n - 1] if isEven else poly[n]]
            newTri.append(attemptedTri) 
            n += 1
        return newTri
            
    elif opcode == 0xA0:
        for i in range(1, len(poly) - 1):
            attemptedTri = [poly[i],
                            poly[i + 1],
                            poly[0]]
            newTri.append(attemptedTri) 
        return newTri
    
    else:
        raise RuntimeError(f"Unhandled opcode {opcode}")
    
    return None

if __name__ == "__main__":
    print("MOD2OBJ\n")

    with open(sys.argv[1], "rb") as modFile:
        mod_sections = SplitModToSections(modFile)
        print("Chunks found:")
        for chunk_id in mod_sections:
            print(hex(chunk_id))
        print()

        obj_file = AL.ObjFile(open("out.obj", "w"))

        # Vertices
        if 0x10 in mod_sections:
            print("Ripping Vertices (0x10)")
            stream = mod_sections[0x10][1]
            vertex_count = stream.readInt32()

            stream.skipPadding()

            for i in range(vertex_count):
                obj_file.add_F32Trio(
                    "v", stream.readFloat(), stream.readFloat(), stream.readFloat()
                )

        # Vertex Normals
        if 0x11 in mod_sections:
            print("Ripping Vertex Normals (0x11)")
            stream = mod_sections[0x11][1]
            vnorm_count = stream.readInt32()
            stream.skipPadding()

            for i in range(vnorm_count):
                obj_file.add_F32Trio(
                    "vn", stream.readFloat(), stream.readFloat(), stream.readFloat()
                )

        # UV maps
        for i in range(8):
            if (0x18 + i) in mod_sections:
                print(f"Ripping Texture Coordinates ({hex(0x18 + i)})")
                stream = mod_sections[0x18 + i][1]
                uv_count = stream.readInt32()
                stream.skipPadding()

                for i in range(uv_count):
                    obj_file.add_F32Duo("vt", stream.readFloat(), stream.readFloat())

        if 0x50 in mod_sections:
            print("Ripping Meshes (0x50)")
            stream = mod_sections[0x50][1]
            
            batch_count = stream.readUInt32()
            stream.skipPadding()
            for batch_num in range(batch_count):
                obj_file.add_comment(f"Batch {batch_num}")
                
                batch_flags = stream.readUInt32()                
                batch_vcd = VertexDescriptor()
                batch_vcd.from_pikmin1(stream.readInt32(), hasNormals = (0x11 in mod_sections))      
                          
                mtx_count  = stream.readUInt32()                
                for mtx_num in range(mtx_count):
                    obj_file.add_comment(f"MTX {mtx_num}")
                    
                    mtx_dep_count = stream.readUInt32()
                    for mtx_dep_num in range(mtx_dep_count):
                        stream.readUInt16()
                    
                    dlist_count = stream.readUInt32()
                    for dlist_num in range(dlist_count):
                        obj_file.add_comment(f"Display List {dlist_num}")
                        
                        dlist_flags = stream.readUInt32()
                        dlist_unk = stream.readUInt32()
                        dlist_size = stream.readUInt32()
                        
                        stream.skipPadding()

                        dlist_start = stream.tell()
                        dlist_data = stream.readX(dlist_size)
                        dlist_end = stream.tell()
                        
                        stream.seek(dlist_start)
                        
                        while stream.tell() < dlist_end:
                            opcode = stream.readUInt8()
                            if opcode == 0x98 or opcode == 0xA0:
                                faceCount = stream.readUInt16()
                                cPoly = []
                                cPolyAppend = cPoly.append
                                for face_num in range(faceCount):
                                    for attr, format in batch_vcd.active_attributes():
                                        if attr == VTX.Position:
                                            cPolyAppend(stream.readUInt16() + 1)
                                        elif format is None:
                                            stream.readUInt8()
                                        elif format == VTXFMT.INDEX16:
                                            stream.readUInt16()
                                        else:
                                            raise RuntimeError(f"Unexpected format / attribute ({attr}/{format})")
                                    
                                cPoly = ConvertToObjTriangle(cPoly, opcode)
                                for polygon in cPoly:
                                    obj_file.add_U32Trio("f", polygon[0], polygon[1], polygon[2])
                                
                            elif opcode != 0:
                                raise RuntimeError(f"Got unexpected opcode! {opcode}")
                        stream.seek(dlist_end)
        
        # Textures
        if 0x20 in mod_sections:
            print("Ripping Textures (0x20)")
            stream = mod_sections[0x20][1]

            texture_count = stream.readUInt32()

            stream.skipPadding()

            for i in range(texture_count):
                with AL.OpenFileInFolder(
                    "texture_" + str(i) + ".txe", "textures", "wb"
                ) as texture_file:
                    width = stream.readUInt16()
                    height = stream.readUInt16()
                    fmt = stream.readUInt32()
                    unk001 = stream.readUInt32()

                    stream.readUInt32()
                    stream.readUInt32()
                    stream.readUInt32()
                    stream.readUInt32()

                    texture_size = stream.readUInt32()

                    print(
                        f"Texture [{i}] is {width}x{height}, Size of the texture is {texture_size} bytes"
                    )

                    texture_data = stream.readX(texture_size)

                    texture_file.write(struct.pack(">H", width))
                    texture_file.write(struct.pack(">H", height))
                    texture_file.write(struct.pack(">H", unk001))
                    texture_file.write(struct.pack(">H", fmt))
                    texture_file.write(struct.pack(">I", texture_size))

                    for j in range(20):
                        texture_file.write(struct.pack("x"))

                    texture_file.write(texture_data)
                    
                    try:
                        img = image_gc.Image()
                        img.format = img.decodeFormat(fmt)
                        img.width = width
                        img.height = height
                        img.size = texture_size
                        img.loadImage(texture_data)
                        img.saveImage(f"textures/texture{i}.png")
                    except:
                        print(f"Unable to decode Texture[{i}]")
                        pass
        
        
        # INI File
        stream = mod_sections[0xffff][1]
        stream.seek(0x18)
        
        obj_file.close()
