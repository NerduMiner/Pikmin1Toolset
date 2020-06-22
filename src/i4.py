import io
import struct
from bitstring import BitArray
from imageformat import ImageFormat

class I4(ImageFormat):
    def __init__(self, data, width, height):
        self.blockWidth = 8
        self.blockHeight = 8
        self.blockSize = 32
        self.bitsPerPixel = 4
        ImageFormat.__init__(self, data, width, height)
        
    def decodeBlock(self, block):
        bl = []
        s = io.BytesIO(block)
        
        for j in range(0, 8):
            bl.append([])
            for i in range(0, 4):
                pix = BitArray(uint=struct.unpack('>B', s.read(1))[0], length=8)
                into = pix[:4].uint * 17
                intt = pix[-4:].uint * 17
                bl[j].append((into, into, into, 255))
                bl[j].append((intt, intt, intt, 255))
                
        return bl
                