import struct
import PIL.Image
from cmpr import *
from rgb5a3 import *
from rgb565 import *
from rgba8 import *
from i4 import *
from ia8 import *

class Image:
    def __init__(self, header=False, data=False):
        self.size = 0
        
        if header != False: 
            self.loadHeader(header)
        if data != False: 
            self.loadImage(data)
    
    def loadHeader(self, header):
        self.processImageHeader(header)
        return {'offset': self.offset, 'size': self.size}

    def loadImage(self, data):
        if self.format == 'CMPR':
            self.image = CMPR(data, self.width, self.height)
        if self.format == 'IA8':
            self.image = IA8(data, self.width, self.height)
        if self.format == 'RGB5A3':
            self.image = RGB5A3(data, self.width, self.height)
        if self.format == 'RGB565':
            self.image = RGB565(data, self.width, self.height)
        if self.format == 'I4':
            self.image = I4(data, self.width, self.height)
        if self.format == 'RGBA8':
            self.image = RGBA8(data, self.width, self.height)
        
            
    def saveImage(self, filename):
        img = PIL.Image.new('RGBA', (self.width, self.height))
        img.putdata(self.image.getPixels())
        img.save(filename)
        
    def decodeFormat(self, fmat):        
        if fmat == 0:
            return 'RGB5A3'
        if fmat == 1:
            return 'CMPR'
        if fmat == 2:
            return 'RGB565'
        if fmat == 3:
            return 'I4'
        if fmat == 4:
            return 'I8'
        if fmat == 5:
            return 'IA4'
        if fmat == 6:
            return 'IA8'
        if fmat == 8:
            return 'RGBA32'
        
        return False
        
    def processImageHeader(self, data):
        self.height = struct.unpack('>H', data[:2])[0]
        self.width = struct.unpack('>H', data[2:4])[0]
        self.format = self.decodeFormat(data[4:8])
        self.offset = struct.unpack('>I', data[8:12])[0]