from iocbuilder import Device, AutoSubstitution, SetSimulation
from iocbuilder.arginfo import *

from iocbuilder.modules.asyn import AsynPort
from iocbuilder.modules.ADCore import ADCore, ADBaseTemplate, includesTemplates, makeTemplateInstance



class GenICam(AsynPort,):
    '''Creates a aravisCamera camera areaDetector driver'''
    Dependencies = (ADCore,)
    # This tells xmlbuilder to use PORT instead of name as the row ID
    #UniqueName = "PORT"
    def __init__(self, P,R,PORT, ID, CLASS, PV_ALIAS, BUFFERS = 50, MEMORY = -1, **args):
        # Init the superclass
        print"GenICam __init__ called\n"
        print"PORT: "+PORT + " ID: " + ID + " CLASS: " + CLASS + "\n"
        self.__super.__init__(PORT)
        # Update the attributes of self from the commandline args
        self.__dict__.update(locals())
        # Make an instance of our template
        # Backwards compatible Manta

 
        # Init the camera specific class
        class _tmp(AutoSubstitution):
            ModuleName = GenICam.ModuleName
            TrueName = "_%s" % CLASS
            TemplateFile = "%s.template" % CLASS

        class _alias(AutoSubstitution):
            ModuleName = GenICam.ModuleName
            TemplateFile = "PVAlias.template"

        makeTemplateInstance(_tmp, locals(), args)

        if PV_ALIAS > 0:
            makeTemplateInstance(_alias, locals(), args)
        


    # Device attributes
    LibFileList = ['ADGenICam']

