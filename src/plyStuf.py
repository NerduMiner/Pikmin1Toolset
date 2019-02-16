class plyStuf:
    ply = open(self.filename+".ply", 'w+')
    def __init__(self, filename):
        self.filename = name
    def initPLY(self):
        self.write("ply\n")
        self.write("format ascii 1.0\n")
    def defineVertex(self, vertexNum):
        self.write("element vertex "+str(vertexNum)+"\n")
        self.write("property float x\n")
        self.write("property float y\n")
        self.write("property float z\n")
    def defineFace(self, faceNum):
        self.write("element face "+str(faceNum)+"\n")
        self.write("property list uchar int vertex_index\n")
        self.write("end_header\n")
        
