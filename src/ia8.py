import io
import struct
from imageformat import ImageFormat

class IA8(ImageFormat):
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
                col = struct.unpack('>B', s.read(1))[0]
                alpha = struct.unpack('>B', s.read(1))[0]
                bl[j].append((col, col, col, alpha))
                
        return bl
                