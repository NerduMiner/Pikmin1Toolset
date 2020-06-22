import io
import struct
from bitstring import BitArray
from imageformat import ImageFormat

class RGBA8(ImageFormat):
    def __init__(self, data, width, height):
        self.blockWidth = 4
        self.blockHeight = 4
        self.blockSize = 64
        self.bitsPerPixel = 32
        ImageFormat.__init__(self, data, width, height)
        
    def decodeBlock(self, block):
        bl = []
        s = io.BytesIO(block)
        pix = []

        for i in range(0, 16):
            a = struct.unpack('>B', s.read(1))[0]
            r = struct.unpack('>B', s.read(1))[0]
            pix.append({'a': a, 'r': r})
            
        for i in range(0, 16):
            g = struct.unpack('>B', s.read(1))[0]
            b = struct.unpack('>B', s.read(1))[0]
            pix[i]['g'] = g
            pix[i]['b'] = b
        
        for j in range(0, 4):
            bl.append([])
            for i in range(0, 4):
                p = pix[j*4+i]
                bl[j].append((p['r'], p['g'], p['b'], p['a']))
                
        return bl