import struct
import sys
import os
import io
from yoshiStuf import *
from dmdStuf import *
from array import array

faceNum = 0
vertexNum = 0
normNum = 0
array = []
fooce = []
norm = []

with open(sys.argv[1], "r") as obj:
    for line in obj:
        if ('vn') in line:
            if ('###') in line:
                continue
            line = line[2:]
            norm.append([float(x) for x in line.split()])
            normNum += 1
        if ('v') in line:
            if ('###' or '#') in line:
                continue
            line = line[1:]
            array.append([float(x) for x in line.split()])
            #print(array)
            vertexNum += 1
        if ('##') in line:
            if ('###') in line:
                continue
            continue
        if ('#') in line:
            if ('###') in line:
                continue
        if ('f') in line:
            #print(line)
            line = line[1:]
            fooce.append([int(x) for x in line.split()])
            #print(fooce)
            faceNum += 1
    print(str(vertexNum) + " vertices found.")
    print(str(faceNum) + " faces found.")
    print(str(normNum) + " normals found")

dmdWrite = dmdStuf("output")
dmdWrite.initDMD()

if vertexNum > 0:
    dmdWrite.initVert(vertexNum)
    for x in range(vertexNum):
        dmdWrite.addVert(array[x][0], array[x][1], array[x][2])
    dmdWrite.finishVert()
    dmdWrite.completeSection()

if normNum > 0:
    dmdWrite.initNorm(normNum)
    for x in range(normNum):
        dmdWrite.addNorm(norm[x][0], norm[x][1], norm[x][2])
    dmdWrite.completeSection()

if faceNum > 0:
    dmdWrite.initPoly(faceNum)
    for x in range(faceNum):
        dmdWrite.addPoly(fooce[x][0], fooce[x][1], fooce[x][2])
    dmdWrite.completeSection()
