# airconics_setup.py Setup file: here you can specify top level system variables 
# ==============================================================================
# AirCONICS
# Aircraft CONfiguration through Integrated Cross-disciplinary Scripting 
# version 0.2.1
# Andras Sobester, 2015.
# Bug reports to a.sobester@soton.ac.uk or @ASobester please.
# ==============================================================================
import sys
import os

# *** There are NO entries to edit here ***

# Check if using unix style system or windows:
if os.name in ['posix','mac']:
	RhinoVersion = 2
elif os.name == 'nt':
	RhinoVersion = 1

# ONE:
# The string below should contain the path to your installation of AirCONICS
# Example: AirCONICSpath = "D:/Projet HN Rhino/3DRhino_parametric_foils/AirCONICS-master"
AirCONICSpath = os.getcwd() + '/'

# TWO:
# The string below should contain the path to your library of Selig-formatted
# airfoils. If you are using the UIUC library included in this installation,
# this should be the path to the Sections folder included.

# Example: SeligPath = "D:/HN Rhino/3DRhino_parametric_foils/AirCONICS-master/AirCONICS-master/"
SeligPath = AirCONICSpath + '../Sections/'

os.listdir(SeligPath)



# ==============================================================================
print("System variables initialised.")
if AirCONICSpath not in sys.path:
	sys.path.append(AirCONICSpath)
