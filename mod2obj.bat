@echo off
mkdir output
cd output
python "../src/__mod2obj.py" %1 > objWriteLog.txt