#Makefile at top of application tree
TOP = .
include $(TOP)/configure/CONFIG
DIRS := $(DIRS) configure
DIRS := $(DIRS) GenICamApp
DIRS := $(DIRS) scripts
include $(TOP)/configure/RULES_TOP
