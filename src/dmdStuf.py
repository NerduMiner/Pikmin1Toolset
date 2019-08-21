class dmdStuf:
    """Contains the methods needed to create a .dmd file"""

    def __init__(self, filename):
        self.filename = filename
        self.dmd = open(filename + ".dmd", 'w+')
        self.temp = open(filename + ".tmp", 'w+')
        self.vert1Min = 0
        self.vert1Max = 0
        self.Min = 0
        self.Max = 0

    def initDMD(self):
        """Creates the header of the model file, placeholder values used"""
        self.dmd.write("<INFORMATION>\n{")
        self.dmd.write("       version 3.109\n")
        self.dmd.write("        filename        D:/" + self.filename + "\n")
        self.dmd.write("        toolname        Maya\n")
        self.dmd.write("        source  'Maya 4.0.1 - (file.mb)'\n")
        self.dmd.write("        date    2019/8/19\n")
        self.dmd.write("        time    12:50:24\n")
        self.dmd.write("        host    DMD2MOD\n")
        self.dmd.write("        magnify 1.000000\n")
        #self.dmd.write("        suitable_joint  cull    3\n")
        self.dmd.write("        numjoints        0\n")
        self.dmd.write("        scalingrule      maya\n")
        self.dmd.write("        primitive        TriangleList\n")
        self.dmd.write("        embossbump       off\n")
        self.dmd.write("        compress_mat     off\n")
        self.dmd.write("        vtxclranm        nouse\n}\n")

    def initVert(self, vertexNum):
        """Sets up the first part of the <VTX_POS> section of the model"""
        self.dmd.write("<VTX_POS>\n{\n")
        self.dmd.write("        size    " + str(vertexNum) + "\n")

    def finishVert(self):
        """Completes the header of <VTX_POS> and adds the data"""
        self.dmd.write("        min    " + self.Min + "\n")
        self.dmd.write("        max    " + self.Max + "\n\n")
        self.temp.close()
        temp = open(self.filename + ".tmp", 'r')
        data = temp.read()
        for line in data:
            self.dmd.write(line)

    def completeSection(self):
        """Use to wrap up a section in the model when done"""
        self.dmd.write("}\n\n\n")

    def addVert(self, vert1, vert2, vert3):
        self.temp.write(f'        float {str(vert1)} {str(vert2)} {str(vert3)} \n')
        if vert1 < self.vert1Min:
            self.vert1Min = vert1
            self.Min = f'{str(vert1)} {str(vert2)} {str(vert3)}'
        elif vert1 > self.vert1Max:
            self.vert1Max = vert1
            self.Max = f'{str(vert1)} {str(vert2)} {str(vert3)}'

    def initNorm(self, normNum):
        """Sets up the <VTX_NRM> section of the model"""
        self.dmd.write("<VTX_NRM>\n{\n")
        self.dmd.write("        size    " + str(normNum) + "\n\n")

    def addNorm(self, norm1, norm2, norm3):
        self.dmd.write(f'        float {str(norm1)} {str(norm2)} {str(norm3)} \n')

    def initPoly(self, faceNum):
        """Set up the the <POLYGON> section [PLACEHOLDER VALUES USED]"""
        self.dmd.write("<POLYGON>\n{\n")
        self.dmd.write("\tindex   0\n")
        self.dmd.write("\tlight   on\n")
        self.dmd.write("\tembossbump off\n")
        #self.dmd.write("\tvolume_min " + str(self.Min) + "\n")
        #self.dmd.write("\tvolume_max " + str(self.Max) + "\n")
        #self.dmd.write("\tvolume_r   " + str(self.vert1Max + 10) + "\n")
        # vcd_data is a 21 number array for these vertex descriptors in this order:
        # position matrix, tex0-tex7 matrix, vertex position, normal, color0, color1, tex0 to tex7 coordinates
        self.dmd.write("\tvcd 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0\n")
        #self.dmd.write("\ttotal_nodes " + str(faceNum) + "\n")
        self.dmd.write("\tnmtx_lists 0\n")
        self.dmd.write("\tnmtxs  0\n")
        #self.dmd.write("\tnnodess " + str(faceNum) + "\n")
        self.dmd.write("\tface    front\n")

    def addPoly(self, poly1, poly2, poly3):
        """Add the face data into a node"""
        self.dmd.write("\tnodes   3\n")
        self.dmd.write("\tvcd_dat -1 -1 -1 -1 -1 -1 -1 -1 -1 " + str(poly1 - 1) + " -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1\n")
        self.dmd.write("\tvcd_dat -1 -1 -1 -1 -1 -1 -1 -1 -1 " + str(poly2 - 1) + " -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1\n")
        self.dmd.write("\tvcd_dat -1 -1 -1 -1 -1 -1 -1 -1 -1 " + str(poly3 - 1) + " -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1\n")
