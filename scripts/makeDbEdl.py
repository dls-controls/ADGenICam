#!/bin/env python
import os, sys, re
from subprocess import Popen, PIPE
from xml.dom.minidom import parseString
from optparse import OptionParser

# Location of script to convert adl to edl screens
adl2edlLocation="/dls_sw/prod/tools/RHEL7-x86_64/adl2edl/1-7/prefix/bin/adl2edl"

# Strings to swap to convert color scheme to diamond. Need to find a nicer way to do this.
adlMessageButton = """fgColor index 14\nonColor index 51\noffColor index 51\ntopShadowColor index 0\nbotShadowColor index 14"""
adlMenuButton = """bgColor index 51\ninconsistentColor index 12\ntopShadowColor index 2\nbotShadowColor index 12"""
adlTitle = """w 1460\nh 24\nfont "helvetica-bold-r-12.0"\nfontAlign "center"\nfgColor index 14\nbgColor index 3\nuseDisplayBg"""
adlRect="""lineColor index 14\nfillColor index 14\nlineWidth 0\nendObjectProperties\n"""
adlTextMon="""fgColor index 15\nbgColor index 12\nlimitsFromDb\n"""

edmMessageButton="""fgColor index 25\nonColor index 3\noffColor index 3\ntopShadowColor index 1\nbotShadowColor index 11"""
edmMenuButton = """bgColor index 3\ninconsistentColor index 25\ntopShadowColor index 1\nbotShadowColor index 11"""
edmTitle = """w 1460\nh 24\nfont "helvetica-bold-r-12.0"\nfontAlign "center"\nfgColor index 14\nbgColor index 48"""
edmRect="""lineColor index 14\nfill\nfillColor index 5\nlineWidth 0\nendObjectProperties\n"""
edmTextMon="""fgColor index 15\nbgColor index 10\nlimitsFromDb\n"""


# parse args
parser = OptionParser("""%prog <xmlFile> <templateFile>

This script parses a genicam xml file and creates a database template""")
options, args = parser.parse_args()
if len(args) != 1:
    parser.error("Incorrect number of arguments")

# Get all relevant file names
xml_filename = args[0]
db_filename = args[0].split('/')[-1].replace("xml","template")
edl_filename = db_filename.replace("template","edl")

# Create the template file
os.system(f'dls-python makeDb.py {args[0]} {db_filename}')

# Move the tempate file into final location
os.system(f'mv {db_filename} ../db/')

# Make the adl file ready for conversion
os.system(f'dls-python makeAdl.py {args[0]} {edl_filename.replace(".edl","")}')


featureScreens = list()

# Get a list of all the adl feature screens
stdout = Popen('ls | grep features', shell=True, stdout=PIPE).stdout
featureScreens = stdout.read().split()

# Convert each screen found to edl, replace various strings in the file to make
# the color scheme match diamond
for screen in featureScreens:
    print(screen)
    os.system(f'{adl2edlLocation} {screen.decode()} > {screen.decode().replace(".adl",".edl")}')
    fin = open(screen.decode().replace(".adl",".edl"),"r")
    data = fin.read()
    data = data.replace(adlMenuButton,edmMenuButton)
    data = data.replace(adlMessageButton,edmMessageButton)
    data = data.replace(adlTitle,edmTitle)
    data = data.replace(adlRect,edmRect)
    data = data.replace(adlTextMon,edmTextMon)
    data = data.replace("helvetica","arial")
    fin.close
    fin = open(screen.decode().replace(".adl",".edl"),"w")
    fin.write(data)
    fin.close
    # Move screens to final location
    os.system(f'mv {screen.decode().replace(".adl",".edl")} ../data/')
    # Delete any junk left by the other scripts
    os.system(f'rm {screen.decode()} {screen.decode().replace(".adl",".adl.db")}')


#print()
#endObjectProperties""" % globals() )

