import sys
import struct
import io

# YL | YOSHI2 LIBRARY

class bStream():
    def __init__(self, f):
        self.fhandle = f
        self.decoder = 'shift-jis'
        
    def __init__(self, bytes):
        self.fhandle = io.BytesIO(bytes)
        self.decoder = 'shift-jis'
        
    def readStr(self, len=0, nullTerm=False):
        if (not nullTerm):
            return self.fhandle.read(len).decode(self.decoder)   
        else:
            tString = b''
            curr = self.fhandle.read(1)
            while (curr != b'' and struct.unpack(">B", curr)[0] != 0):
                try:
                    tString += curr
                except Exception as e:
                    print('Error "{0}" while reading string at {1}'.format(e, hex(self.fhandle.tell())))
                curr = self.fhandle.read(1)
            return tString.decode(self.decoder)

    def readX(self, length):
        return self.fhandle.read(length)

    def readUInt32(self):
        return struct.unpack('>I', self.fhandle.read(4))[0]

    def readInt32(self):
        return struct.unpack('>i', self.fhandle.read(4))[0]
        
    def readUInt32(self):
        return struct.unpack('>I', self.fhandle.read(4))[0]
        
    def readUInt16(self):
        return struct.unpack('>H', self.fhandle.read(2))[0]

    def readInt16(self):
        return struct.unpack('>h', self.fhandle.read(2))[0]

    def readUInt8(self):
        return struct.unpack('>B', self.fhandle.read(1))[0]

    def readInt8(self):
        return struct.unpack('>b', self.fhandle.read(1))[0]

    def readFloat(self):
        return round(struct.unpack('>f', self.fhandle.read(4))[0], 6)

    def readU32s(self, count):
        ret = []
        for x in range(0, count):
            ret.append(self.readUInt32())
        return ret

    def writeFloat(self, float):
        return struct.pack(">f", float)

    def tell(self):
        return self.fhandle.tell()

    def seekBack(self, whence=0):
        self.fhandle.seek(self.backPos, whence)

    def seek(self, pos, whence=0):
        self.backPos = self.fhandle.tell()
        self.fhandle.seek(pos, whence)

    def skipPadding(self, multiple=0x20, base=0x8):
        fpos = self.fhandle.tell()+base
        if fpos % multiple == 0:
            return
        skipto = (fpos - (fpos % multiple)) + multiple 
        skipdiff = skipto - self.fhandle.tell() - base
        self.fhandle.read(skipdiff)
    
        return skipdiff

    def packRead(self, length):
        dataList = []
        dataListAppend = dataList.append
        for x in range(length):
            dataListAppend(self.fhandle.read(1))
        return dataList

    def close(self):
        self.fhandle.close()