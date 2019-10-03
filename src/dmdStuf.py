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
        self.index = 0

    def initDMD(self):
        """Creates the header of the model file, placeholder values used"""
        self.dmd.write("<INFORMATION>\n{")
        self.dmd.write("\tmagnify 1.000000\n")
        self.dmd.write("\tnumjoints\temp1\n")
        self.dmd.write("\tscalingrule\tsoftimage\n") # can only be on (classic scaling system), else softimage scaling system
        self.dmd.write("\tprimitive\tTriangleStrip\n") # can only be trianglestrip, otherwise its something else lol idk
        self.dmd.write("\tembossbump\toff\n")
        self.dmd.write("}\n\n")

    def completeSection(self):
        """Use to wrap up a section in the model that has variable length when done"""
        self.dmd.write("}\n\n\n")

    def addMatrix(self):
        self.dmd.write("<VTX_MATRIX>\n{\n")
        self.dmd.write("\tsize\t1\n")
        self.dmd.write("\tmatrix full\t0\n}\n\n\n")

    def initVert(self, vertexNum):
        """Sets up the first part of the <VTX_POS> section of the model"""
        self.dmd.write("<VTX_POS>\n{\n")
        self.dmd.write("\tsize\t" + str(vertexNum) + "\n")

    def addVert(self, vert1, vert2, vert3):
        self.temp.write(f'\tfloat {str(vert1)} {str(vert2)} {str(vert3)} \n')
        if vert1 < self.vert1Min:
            self.vert1Min = vert1
            self.Min = f'{str(vert1)} {str(vert2)} {str(vert3)}'
        elif vert1 > self.vert1Max:
            self.vert1Max = vert1
            self.Max = f'{str(vert1)} {str(vert2)} {str(vert3)}'

    def finishVert(self):
        """Completes the header of <VTX_POS> and adds the data"""
        self.dmd.write("\tmin\t" + self.Min + "\n")
        self.dmd.write("\tmax\t" + self.Max + "\n\n")
        self.temp.close()
        temp = open(self.filename + ".tmp", 'r')
        data = temp.read()
        for line in data:
            self.dmd.write(line)

    def initEnvenlope(self, vertexNum):
        self.dmd.write("<ENVELOPE_XYZ>\n{\n")
        self.dmd.write("\tsize\t" + str(vertexNum) + "\n")
        self.dmd.write("\tmin\t" + self.Min + "\n")
        self.dmd.write("\tmax\t" + self.Max + "\n")

    def initDeformed(self, vertexNum):
        self.dmd.write("<DEFORMED_XYZ>\n{\n}")
        self.dmd.write("\tsize\t" + str(vertexNum) + "\n")
        self.dmd.write("\tmin\t" + self.Min + "\n")
        self.dmd.write("\tmax\t" + self.Max + "\n")

    def initNorm(self, normNum):
        """Sets up the <VTX_NRM> section of the model"""
        self.dmd.write("<VTX_NRM>\n{\n")
        self.dmd.write("\tsize\t" + str(normNum) + "\n\n")

    def addNorm(self, norm1, norm2, norm3):
        self.dmd.write(f'\tfloat {str(norm1)} {str(norm2)} {str(norm3)} \n')

    def initEnNorm(self, normNum):
        self.dmd.write("<ENVELOPE_NRM>\n{\n")
        self.dmd.write("\tsize\t" + str(normNum) + "\n\n")

    def initTexCoord(self, texNum, uvSize):
        self.dmd.write("<TEXCOORD" + str(texNum) + ">\n{\n")
        self.dmd.write("\tmin 0.000000 0.000000\n")
        self.dmd.write("\tmax 1.000000 1.000000\n\n\n")

    def addUVTexCoord(self, u, v):
        self.dmd.write(f"\tfloat\t{str(u)} {str(v)}\n")

    def initMaterial(self, texName):
        self.dmd.write("<MATERIAL>\n{\n")
        self.dmd.write("\tindex\t" + str(self.index) + "\n")
        self.index +=1
        self.dmd.write("\tname \t" + str(texName) + "\n")
        self.dmd.write("\tcol_source  both\n")
        self.dmd.write("\tapl_source  both\n")
        self.dmd.write("\tmode\tEDG\n")
        for x in range(8):
            self.dmd.write(f"\ttexture{x}\t-1")

    def initPoly(self, faceNum):
        """Set up the the <POLYGON> section [PLACEHOLDER VALUES USED]"""
        self.dmd.write("<POLYGON>\n{\n")
        self.dmd.write("\tindex\t0\n")
        self.dmd.write("\tlight\ton\n")
        self.dmd.write("\tembossbump\toff\n")
        # vcd_data is a 21 number array for these vertex descriptors in this order:
        # position matrix, tex0-tex7 matrix, vertex position, normal, color0, color1, tex0 to tex7 coordinates
        self.dmd.write("\tvcd 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0\n")
        #self.dmd.write("\ttotal_nodes " + str(faceNum) + "\n")
        self.dmd.write("\tnmtx_lists\t" + str(faceNum) + "\t0 0 0\n")
        #self.dmd.write("\tnnodess " + str(faceNum) + "\n")
        self.dmd.write("\tface\tfront\n")

    def addPoly(self, poly1, poly2, poly3):
        """Add the face data into a node"""
        self.dmd.write("\tnodes\t3\n")
        self.dmd.write("\tvcd_dat -1 -1 -1 -1 -1 -1 -1 -1 -1 " + str(poly1 - 1) + " -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1\n")
        self.dmd.write("\tvcd_dat -1 -1 -1 -1 -1 -1 -1 -1 -1 " + str(poly2 - 1) + " -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1\n")
        self.dmd.write("\tvcd_dat -1 -1 -1 -1 -1 -1 -1 -1 -1 " + str(poly3 - 1) + " -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1\n")

    def addRootJoint(self):
        """Add a root joint to the dmd model, which is needed"""
        self.dmd.write("<JOINT>\n{\n")
        self.dmd.write("\tindex\t0\n")
        self.dmd.write("\tname\ttop3\n")
        self.dmd.write("\tkind\tmesh\n")
        self.dmd.write("\tparent\t-1\t(null)\n")
        self.dmd.write("\tchild\t-1\t(null)\n")
        self.dmd.write("\tbrother_next\t-1\t(null)\n")
        self.dmd.write("\tbrother_prev\t-1\t(null)\n\n")
        self.dmd.write("\tdraw_mtx\tuse\n")
        self.dmd.write("\tscale_compensate\toff\n")
        self.dmd.write("\tscaling 1.000000 1.000000 1.000000\n")
        self.dmd.write("\trotation\t0.000000 0.000000 0.000000\n")
        self.dmd.write("\ttranslation 0.000000 0.000000 0.000000\n")
        self.dmd.write("\tbillboard\toff\n")
        self.dmd.write("\tvolume_min\t" + str(self.Min) + "\n")
        self.dmd.write("\tvolume_max\t" + str(self.Max) + "\n")
        self.dmd.write("\tvolume_r\t" + str(self.vert1Max + 10) + "\n")
        self.dmd.write("\tndisplays\t1\n")
        self.dmd.write("\tdisplay 0 0\n}")
