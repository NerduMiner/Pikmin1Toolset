@echo off
mkdir output
cd output
python "src/__obj2mod.py" %1 > modWriteLog.txt