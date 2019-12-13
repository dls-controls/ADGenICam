#!/bin/env python
import os, sys, re
from subprocess import Popen, PIPE


stdout = Popen('ls ../xml | grep .xml', shell=True, stdout=PIPE).stdout

xmlFiles = stdout.read().split()

os.system(f'rm ../convert.err')

for camera in xmlFiles:
    print(f'Converting {camera.decode()}')
    os.system(f'dls-python3 makeDbEdl.py ../xml/{camera.decode()} &>> ../convert.err')
