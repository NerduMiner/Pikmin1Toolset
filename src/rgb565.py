import io
import struct
from bitstring import BitArray
from imageformat import ImageFormat

class RGB565(ImageFormat):
    def __init__(self, data, width, height):
        self.blockWidth = 4
        self.blockHeight = 4
        self.blockSize = 32
        self.bitsPerPixel = 16
        ImageFormat.__init__(self, data, width, height)
        
    def decodeBlock(self, block):
        bl = []
        s = io.BytesIO(block)
        
        for j in range(0, 4):
            bl.append([])
            for i in range(0, 4):
                pix = BitArray(uint=struct.unpack('>H', s.read(2))[0], length=16)
                r = self.colourScale(pix[:5].uint, 32)
                g = self.colourScale(pix[5:11].uint, 64)
                b = self.colourScale(pix[11:16].uint, 32)
                bl[j].append((r, g, b, 255))
                
        return bl