# LEModeler

LEModeler is an open-source tool for automatically generating and exporting parametric hydrofoil geometries using the Rhinoceros 3D CAD engine.

#
## Credit
Developed and provided by Hugo Nicolas - [hugo.nicolas@polytechnique.edu](mailto:hugo.nicolas@polytechnique.edu)

Based on the book [Aircraft Aerodynamic Design - Geometry and Optimization](https://www.wiley.com/en-gb/Aircraft+Aerodynamic+Design%3A+Geometry+and+Optimization-p-9780470662571) by András Sóbester and Alexander I J Forrester.
A library of aircraft geometry codes in Matlab to accompany the book is available [here](https://github.com/sobester/airgeobookcode_m).
A library of Python 2.7 scripts for building aircraft geometries is available [here](https://github.com/sobester/AirCONICS).

# 
## Prerequisites
An installed version of [Rhinoceros3D](https://www.rhino3d.com/en/) (Rhino 6 or higher) is required to run the modeling tool.

For the time being, the tool only runs on Windows.

#
## Folder contents 
The main folder (the LEModeler folder) contains the following elements:
- a folder called "Exports", which contains the exported parts (if any) of modeled foils,
- a folder called "PythonFiles", which contains the *.py* files used for modeling a foil,
- *Sections.zip*, which contains a list of sections (*.dat* in the Selig format) to be used for modeling a foil,
- *foil_dimensions_scheme.png*, which is a scheme of a typical T-foil and its dimensions,
- *input_parameters.txt*, which contains the input parameters,
- *run.bat*, which launches the modeling,
- *LICENSE*, which contains the license,
- *README.md*, which you are carefully reading.

The "PythonFiles" folder contains the following scripts:
- *main.py*, which is the main Python script, the one run by Rhino when launching *run.bat*,
- *Class_X.py*, which are classes called for modeling a foil (the code is object-oriented),
- *Dimensions.py*, which extracts information from *input_parameters.txt*,
- *airconics_setup.py*, which is a setup file,
- *AirCONICStools.py*, which contains ancillary methods called by the higher level AirCONICS functions,
- *liftingsurface.py*, which contains the definition of the class of 3D lifting surfaces,
- *primitives.py*, which contains the definitions of classes of essential 2D geometrical primitives required to construct foil geometries.

These scripts use the *rhinoscriptsyntax* library.

#
## Procedure 
First, unzip *Sections.zip* to get the "Sections" folder within the main folder. It must be named "Sections" such that its directory is "C:\Users\YourUserName\path\to\LEModeler\Sections\airfoil_example.dat". It contains a list of foil cross-sections (see [Cross-sections](#cross-sections)).

The procedure for modeling and exporting a foil is the following:
- 0. Configure *run.bat* (see the dedicated section [Configuration](#configuration)),
- 1. Define the input parameters (see the dedicated section [Input parameters](#input-parameters)),
- 2. Launch the modeling tool by double-clicking on *run.bat* (once configurated, see step 0.),
- 3. The exported parts of the modeled foil are available in the "Exports" folder (see the dedicated section [Export](#export)).

In step 2., *run.bat* launches Rhino and runs *main.py* which, in turn, instantiates a foil whose components are defined by the user in *input_parameters.txt*. If desired, the user can decide to run *main.py* directly from Rhino by following the procedure below:
- 2.1. Open Rhino manually,
- 2.2. Type *RunPythonScript* in the command prompt,
- 2.3. Fetch *main.py* and open it. 

Once modeled, each part represented by its corresponding polysurface is exported to the format(s) defined by the user in *input_parameters.txt*.
Finally, Rhino is closed automatically if set up by the user (see the dedicated section [Input parameters](#input-parameters)).

#
## Configuration
Configure *run.bat* by editing it. It contains the line below.

```
C:\"Program Files"\"Rhino X"\System\Rhino.exe /nosplash /runscript="-_RunPythonScript C:\Users\YourUserName\path\to\LEModeler\PythonFiles\main.py"
```

Make sure to update the following elements accordingly:
- the path to Rhino,
- the version of Rhino (e.g., from Rhino X to Rhino 7),
- the path to the current folder (the LEModeler folder).

#
## Input parameters

To define the input parameters for modeling a hydrofoil, edit *input_parameters.txt*. It contains the sections below.

### **Foil parts to model**
```
----------------------------------------------------------------------------------
wing = yes
stab = yes
mast = no
fuselage = no
----------------------------------------------------------------------------------
```
A T-foil is composed of four parts (namely the front wing, the stabilizer, the mast, and the fuselage). Thus, the lines above allow the user to indicate which foil parts are to be computed by the modeler.
In this example, only the front wing (referred to as "wing") and the stabilizer (referred to as "stab") will be modeled. That is, a "yes" enables the modeling, whereas a "no" prevents it.
The purpose is to save computational time while extending the types of geometries that can be modeled beyond just T-foils (e.g., L-foils) simply by playing with the front wing. T-foil geometries being complex, they serve as a reference.

### **Is the front wing symmetric?**
```
----------------------------------------------------------------------------------
symmetric = yes
----------------------------------------------------------------------------------
```
In this section is defined whether the front wing is symmetric. That is, a "yes" means that the front wing is symmetric. In this case, the front wing span is twice the value of K, the front wing semispan defined in *foil_dimensions_scheme.png* (see [Global dimensions](#global-dimensions)). On the other hand, a "no" means that the front wing is not symmetric. In this case, the front wing is one-sided. Consequently, the front wing span is equal to K.

### **Close Rhino automatically?**
```
----------------------------------------------------------------------------------
close = no
----------------------------------------------------------------------------------
```
In this section is defined whether Rhino will be closed automatically after generating the foil. That is, a "yes" closes Rhino automatically, which may be suited to an optimization framework. On the other hand, a "no" allows one to visualize the foil after the modeling.

### **Global dimensions**
```
----------------------------------------------------------------------------------
width of the upper part of the mast, D = 0.1202
width of the lower part of the mast, G = 0.1059
length of the upper part of the mast, C = 0.2
length of the lower part of the mast, F = 0.6
----------------------------------------------------------------------------------
front wing semispan, K = 0.3
root chord of the front wing, R = 0.1
tip chord of the front wing, S = 0.1
distance between the front wing and the mast, P = 0.11
----------------------------------------------------------------------------------
stabilizer semispan, M = 0.1
root chord of the stabilizer, L = 0.045
tip chord of the stabilizer, T = 0.045
distance between the stabilizer and the mast, O = 0.4
----------------------------------------------------------------------------------
fuselage thickness, H = 0.03
length of the front part of the fuselage, Q = 0.05
length of the rear part of the fuselage, V = 0.555
----------------------------------------------------------------------------------
```
In this section are given the dimensions of the foil such as defined in *foil_dimensions_scheme.png*. 
The dimensions are in m. They can either be integers (i.e., without decimal points) or floats (i.e., with decimal points).
The semispan of the front wing is given by the variable K, such that the span is equal to 2K.
    

### **Angles**
```
----------------------------------------------------------------------------------
dihedral angle of the front wing, dw = -20
sweep angle of the front wing, sw = 3
twist angle of the front wing, tw = 0
angle of attack of the front wing, aoaw = 3
----------------------------------------------------------------------------------
dihedral angle of the stabilizer, dbw = 10
sweep angle of the stabilizer, sbw = 2
twist angle of the stabilizer, tbw = 0
angle of attack of the stabilizer, aoabw = 2
----------------------------------------------------------------------------------
```
In this section are given the local and global angles of rotation of the foil wings.
The angles are in degrees. They can either be integers (i.e., without decimal points) or floats (i.e., with decimal points).
- dw (resp. dbw) denotes the dihedral angle for the front wing (resp. the stabilizer), which is positive for an upward angle. 
- sw (resp. sbw) denotes the sweep angle for the front wing (resp. the stabilizer),
- tw (resp. tbw) denotes the twist angle for the front wing (resp. the stabilizer), which is defined and thus rotates around the trailing edge of the root section so to washout (positive twist angle means a reduction in angle of attack spanwise),
- aoaw (resp. aoabw) denotes the angle of attack for the front wing (resp. the stabilizer), which is defined and thus rotates around the trailing edge of the root section.

### **Span discretization**
```
----------------------------------------------------------------------------------
discretization along the front wing semispan, numsegw = 20
----------------------------------------------------------------------------------
discretization along the stabilizer semispan, numsegbw = 10
----------------------------------------------------------------------------------
```
In this section, the number of segments used for discretizing is half the span of the foil front wing.
The number of segments must be an integer (i.e., without decimal points). In any case, the algorithm automatically takes the integer part of the number given.

### **Cross-sections**
```
----------------------------------------------------------------------------------
cross-section of the mast = naca0008
cross-section of the front wing = h105
cross-section of the stabilizer = naca66210
cross-section of the front part of the fuselage = fuselage_front_section
cross-section of the rear part of the fuselage = fuselage_rear_section
----------------------------------------------------------------------------------
```
In this section are listed the names of the cross-section for each foil part.
Therefore, in the current version of the modeling tool, each part can only be composed of one cross-sectional profile.
In this example, the mast cross-section is a NACA 4-digit profile (namely NACA 0008) while that of the front wing is a user-defined H105 profile.
Profiles whose name is indicated here must be in the "Sections" folder. 
Consequently, any profile can be added by the user in the aforementioned folder as a *.dat* file following the format:
```
<name>
<longitudinal coordinates> <vertical coordinates>
```
LEModeler is able to model either sharp or blunt trailing edges. A sharp trailing edge is modeled if the airfoil is closed in its corresponding *.dat* file. On the other hand, a part is modeled with a blunt trailing edge if its cross-section is left open in the corresponding *.dat* file.

For example, the following airfoil would be modeled with a sharp trailing edge:
```
NACA 65(2)-215
1.00000     0.00000
0.95020     0.00744
...
0.00406     0.01170
0.00000     0.00000
0.00594     -0.01070
...
0.94980     -0.00112
1.00000     0.00000
```
the leading edge being (0 0) and the trailing edge (1 0).

However, the following airfoil would be modeled with a blunt trailing edge:
```
NACA 0021
1.0000     0.00221
0.9500     0.01412
...
0.0125     0.03315
0.0000     0.00000
0.0125     -0.03315
...
0.9500     -0.01412
1.0000     -0.00221
```
as a gap between y = -0.00221 and y = 0.00221 is left at the trailing edge.


### **Extensions**
```
----------------------------------------------------------------------------------
extension = .stp
extension = .igs
extension = .x_t
----------------------------------------------------------------------------------
```
In this section are given the format extensions in which the modeled foil will be exported.
To add (resp. remove) extensions, add (resp. remove) a line "extension = .xxx". The extensions available for the exports are [those supported by Rhino](https://www.rhino3d.com/en/features/file-formats/).

#
## Export
Once modeled under Rhino, the parts of the foil are exported in formats chosen by the user (see the dedicated section [Extensions](#extensions), in [Input parameters](#input-parameters)). 
That is, for each of the parts mentioned above (e.g., the whole main wing), the corresponding polysurface modeled is exported in the "Exports" folder under the name *part_NAME.xxx*. 
"NAME" denotes the name of the part exported (i.e., wing, stab, mast, or fuselage) while ".xxx" denotes the export format extension (see the dedicated section [Extensions](#extensions), in [Input parameters](#input-parameters)). 

#
## In-depth parameterization
As mentioned in the [Introduction](#LEModeler), the modeling tool was designed to be user-friendly by default. 
However, for whoever wishes to model a specific geometry with higher accuracy, it is possible to modify local parameters within the Python scripts in the "PythonFiles" folder.
That, however, requires knowledge of the Python language and the basics of Non-uniform rational basis spline (NURBS). As for the latter, a practical explanation is given in the dedicated section [Explanation of NURBS](#explanation-of-nurbs). For further information, or merely an introduction to the NURBS theory, refer to the dedicated section **Nonuniform Rational Basis Splines** (p. 60 to 64) in [Aircraft Aerodynamic Design - Geometry and Optimization](https://www.wiley.com/en-gb/Aircraft+Aerodynamic+Design%3A+Geometry+and+Optimization-p-9780470662571) or [The NURBS Book](https://link.springer.com/book/10.1007/978-3-642-97385-7).

#
## Contributing
Pull requests and questions are welcome.
