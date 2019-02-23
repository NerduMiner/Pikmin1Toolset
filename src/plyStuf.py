import os


class plyStuf:
    """Contains the methods needed to create a .ply file"""

    def __init__(self, filename):
        self.filename = filename
        self.ply = open(filename + ".ply", 'w+')
        self.temp = open(filename + ".tmp", 'w+')


    def initPLY(self, modname):
        """Creates the starting part of the header, should run first"""
        self.ply.write("ply\n")
        self.ply.write("format ascii 1.0\n")
        self.ply.write("comment model created with mod2obj\n")
        self.ply.write("comment use this model with "+modname+" in obj2mod\n")

    def defineVertex(self, vertexNum):
        """Creates the second part of the header, should run second when vertexNum is found"""
        self.ply.write("element vertex "+str(vertexNum)+"\n")
        self.ply.write("property float x\n")
        self.ply.write("property float y\n")
        self.ply.write("property float z\n")

    def defineFace(self, faceNum):
        """Creates the last part of the header, should run last when the number of faces is found"""
        self.ply.write("element face "+str(faceNum)+"\n")
        self.ply.write("property list uchar int vertex_index\n")
        self.ply.write("end_header\n")

    def addVert(self, vert1, vert2, vert3):
        self.temp.write(f'{str(vert1)} {str(vert2)} {str(vert3)} \n')

    def addFace(self, poly):
        self.temp.write(f'3 {str(poly[0]-1)} {str(poly[1]-1)} {str(poly[2]-1)}\n')

    def addData(self):
        self.temp.close()
        temp = open(self.filename + ".tmp", 'r')
        data = temp.read()
        for line in data:
            self.ply.write(line)
        # os.remove(self.filename + ".tmp")
