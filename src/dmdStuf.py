class dmdStuf:
    """Contains the methods needed to create a .dmd file"""

    def __init__(self, filename):
        self.filename = filename
        self.dmd = open(filename + ".dmd", 'w+')

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
        self.dmd.write("        suitable_joint  cull    3\n")
        self.dmd.write("        numjoints        0\n")
        self.dmd.write("        scalingrule      maya\n")
        self.dmd.write("        primitive        TriangleStrip\n")
        self.dmd.write("        embossbump       off\n")
        self.dmd.write("        compress_mat     off\n")
        self.dmd.write("        vtxclranm        nouse\n}\n")

    def initVert(self, vertexNum):
        """Sets up the <VTX_POS> section of the model"""
        self.dmd.write("<VTX_POS>\n{\n")
        self.dmd.write("        size    " + str(vertexNum) + "\n")
        self.dmd.write("        min    -2500 0 -2500\n")
        self.dmd.write("        max    2500 2500 2500\n\n")

    def completeSection(self):
        """Use to wrap up a section in the model when done"""
        self.dmd.write("}\n\n")

    def addVert(self, vert1, vert2, vert3):
        self.dmd.write(f'        float {str(vert1)} {str(vert2)} {str(vert3)} \n')

    def initNorm(self, normNum):
        """Sets up the <VTX_NRM> section of the model"""
        self.dmd.write("<VTX_NRM>\n{\n")
        self.dmd.write("        size    " + str(normNum) + "\n\n")

    def addNorm(self, norm1, norm2, norm3):
        self.dmd.write(f'        float {str(norm1)} {str(norm2)} {str(norm3)} \n')
