import io

class ImageFormat:
    def __init__(self, data, width, height):
        self.width = width
        self.height = height
        self.loadImage(data)
        
    def loadImage(self, data):
        self.createImageArray(self.width, self.height)
        self.decodeBlocks(data)
        
    def decodeBlocks(self, data):
        s = io.BytesIO(data)
        
        for j in range(0, int(self.height/self.blockHeight)):
            for i in range(0, int(self.width/self.blockWidth)):
                block = s.read(self.blockSize)
                decodedBlock = self.decodeBlock(block)
                self.imageArray = self.listCopy2d(self.imageArray, decodedBlock, i*self.blockHeight, j*self.blockWidth)
        
        s.close()
        
    def createImageArray(self, width, height):
        self.imageArray = [[0 for i in range(width)] for j in range(height)]
                            
    def listCopy2d(self, inp, cop, x, y): 
        ox = x
        for row in cop:
            for pix in row:
                inp[y][x] = pix
                x += 1
            y += 1
            x = ox
        
        return inp
        
    def getPixels(self):
        return [x for sublist in self.imageArray for x in sublist]

    def colourScale(self, col, size):
        return int(round(float(col) * (255 / float(size))))