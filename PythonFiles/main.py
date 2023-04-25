import os
import sys
import Rhino
from Rhino.Geometry import *
from Rhino.Input import RhinoGet
from Rhino.Commands import Result
from Rhino.DocObjects import ObjectType
import rhinoscriptsyntax as rs
from scriptcontext import doc

from Class_Stab import Stab
from Class_Wing import Wing
from Class_Foil import Foil
from Class_Mast import Mast
from Class_Fuselage_front import Fuselagefront
from Class_Fuselage_rear import Fuselagerear



def PartsToModel(filename='..\\input_parameters.txt'):
    """ defines the foil parts to model """
    try:
        f = open(filename, 'r+')
    except IOError as e:
        print('Unable to open de file\n', e)
        sys.exit()
    Parts = dict()
    for el in f.readlines():
        el_split = el.split('=')
        if len(el_split) == 2:
            if str(el_split[0]).strip(' ') in ['wing','stab','mast','fuselage']:
                    Parts[str(el_split[0]).strip(' ')] = str(el_split[1]).strip('\n ')
    return Parts


def SaveAsRhinoFile(extension,Parts_foil_export):
    """ exports the whole foil """
    for key_export in Parts_foil_export.keys():
        rs.SelectObject(str(Parts_foil_export[key_export]))
        if os.path.exists('..\\Exports\\part_' + key_export + extension):
            os.remove('..\\Exports\\part_' + key_export + extension)
        path = os.path.abspath('..\\Exports\\part_' + key_export + extension)
        cmd = "_-Export " + path + " _Enter"
        rs.Command(cmd)
        rs.UnselectObjects(str(Parts_foil_export[key_export]))


def ClearRhinoFile():
    """ deletes every surfaces that are not useful polysurfaces """
    arrObjects = rs.AllObjects()
    for el in arrObjects:
        if not rs.IsPolysurface(el):
            rs.DeleteObject(el)


def ClearLayerRhinoFile():
    """ deletes every layers that are empty """
    arrLayers = rs.LayerNames(False)
    for layerName in arrLayers:
        if rs.IsLayerEmpty(layerName):
            rs.DeleteLayer(layerName)


def CreateObjectRhinoFile():
    """ creates a layer for each object within the Rhino file """
    arrObjects = rs.AllObjects()
    i = 0
    for el in arrObjects:
        i = i + 1
        name = "Layer_number_" + str(i)
        rs.EnableRedraw(False)
        rs.AddLayer(name)
        rs.ObjectLayer(el, name)
        rs.LayerVisible(name, True)
        rs.EnableRedraw(True)
    return i



if __name__ == '__main__':
    try :
        rs.Command("-_SelAll")
        rs.Command("-_Delete")
    except:
        pass
    
    """ construction and saving of the foil """

    # Construction 
    rs.UnitSystem(4)  # meters

    Parts = PartsToModel()  # Parts = {"wing":'yes',"stab":'yes',"mast":'yes',"fuselage":'yes'}
    Parts_foil = dict()

    if Parts["wing"] == 'yes':
        # front wing
        wing = Wing()
        Parts_foil["wing"] = wing

    if Parts["stab"] == 'yes': 
        # stabilizer
        stab = Stab()
        Parts_foil["stab"] = stab

    if Parts["mast"] == 'yes':
        # mast
        mast = Mast()
        Parts_foil["mast"] = mast
    
    if Parts["fuselage"] == 'yes':
        # front part of the fuselage (nose)
        fuselagefront = Fuselagefront()
        # rear part of the fuselage
        fuselagerear = Fuselagerear()
        fuselage = [fuselagefront, fuselagerear]
        Parts_foil["fuselage"] = fuselage

    # whole foil
    foil = Foil(Parts_foil)
    id_Parts_foil = foil.make_foil(Parts_foil)
    Parts_foil_export = dict()

    if "wing" in Parts_foil.keys():
        """ closed front wing """
        id_wing = id_Parts_foil["wing"]
        try:  # blunt trailing edge  
            if foil.symmetric == 'no':
                curve_wing = rs.DuplicateEdgeCurves(id_wing)  # in : str - out : array of strings
                # 0 left, 1 bottom, 2 right, 3 top
                id_patch_wing = rs.AddEdgeSrf((curve_wing[0], curve_wing[2]))  # in : array - out : str
                id_full_wing = rs.JoinSurfaces((id_patch_wing, id_wing), True)
                curve_wing_new = rs.DuplicateEdgeCurves(id_full_wing)
                id_patch_wing_bot = rs.AddEdgeSrf((curve_wing_new[0], curve_wing_new[5]))  # in : array - out : array
                id_patch_wing_top = rs.AddEdgeSrf((curve_wing_new[2], curve_wing_new[4]))
                # array of strings  # 0 left, 1 bottom, 2 right, 3 top, 4 bottom trailing edge, 5 top trailing edge
                front_wing_export = rs.JoinSurfaces((id_full_wing, id_patch_wing_bot, id_patch_wing_top), True)  # in : array - out : str                
                # in : str - out : str
                Parts_foil_export["wing"] = front_wing_export
            elif foil.symmetric == 'yes':
                # right
                curve_wing = rs.DuplicateEdgeCurves(id_wing)  # in : str - out : array of strings
                # 0 left, 1 bottom, 2 right, 3 top
                id_patch_wing = rs.AddEdgeSrf((curve_wing[0], curve_wing[2]))  # in : array - out : str
                id_full_wing = rs.JoinSurfaces((id_patch_wing, id_wing), True)  # in : array - out : str
                curve_wing_new = rs.DuplicateEdgeCurves(id_full_wing)
                id_patch_wing_bot = rs.AddEdgeSrf((curve_wing_new[2], curve_wing_new[4]))
                # array of strings  # 0 left, 1 bottom, 2 right, 3 top, 4 bottom trailing edge, 5 top trailing edge
                id_full_wing_new = rs.JoinSurfaces((id_full_wing, id_patch_wing_bot), True)  # in : array - out : str
                # left
                id_full_wing_mirror = rs.MirrorObject(id_full_wing_new, (-10, 0, -10), (10, 0, 10), True)
                # in : str - out : str
                front_wing_export = rs.JoinSurfaces((id_full_wing_new, id_full_wing_mirror), True)  # in : array - out : str
                Parts_foil_export["wing"] = front_wing_export
        except:  # sharp trailing edge 
            if foil.symmetric == 'no':
                curve_wing = rs.DuplicateEdgeCurves(id_wing)  # in : str - out : array of strings
                id_patch_wing_bot = rs.AddPlanarSrf((curve_wing[1]))  # in : array - out : array
                id_patch_wing_top = rs.AddPlanarSrf((curve_wing[2]))  # in : array - out : array
                front_wing_export = rs.JoinSurfaces((id_patch_wing_bot, id_patch_wing_top, id_wing), True)
                Parts_foil_export["wing"] = front_wing_export
                rs.DeleteObject(id_wing)
                rs.DeleteObject(id_patch_wing_top)
                rs.DeleteObject(id_patch_wing_bot)
            elif foil.symmetric == 'yes':
                # right
                curve_wing = rs.DuplicateEdgeCurves(id_wing)  # in : str - out : array of strings
                id_patch_wing = rs.AddPlanarSrf((curve_wing[1]))  # in : array - out : array
                id_full_wing = rs.JoinSurfaces((id_patch_wing[0], id_wing), True)  # in : array - out : str
                # left
                id_full_wing_mirror = rs.MirrorObject(id_full_wing, (-10, 0, -10), (10, 0, 10), True)
                # in : str - out : str
                front_wing_export = rs.JoinSurfaces((id_full_wing, id_full_wing_mirror), True)  # in : array - out : str
                Parts_foil_export["wing"] = front_wing_export
                # surface deletion
                rs.DeleteObject(id_wing)
                rs.DeleteObject(id_full_wing)
                rs.DeleteObject(id_full_wing_mirror)

    if "stab" in Parts_foil.keys():
        id_stab = id_Parts_foil["stab"]
        """ closed stabilizer """
        try:
            # right
            curve_stab_0 = rs.DuplicateEdgeCurves(id_stab)
            # array of strings  # 0 left, 1 bottom, 2 right, 3 top
            id_patch_stab = rs.AddEdgeSrf((curve_stab_0[0], curve_stab_0[2]))
            id_full_stab_0 = rs.JoinSurfaces((id_patch_stab, id_stab), True)
            curve_stab = rs.DuplicateEdgeCurves(id_full_stab_0)
            id_patch_stab_bot = rs.AddEdgeSrf((curve_stab[2], curve_stab[4]))
            # array of strings  # 0 left, 1 bottom, 2 right, 3 top, 4 bottom trailing edge, 5 top trailing edge
            id_full_stab = rs.JoinSurfaces((id_full_stab_0, id_patch_stab_bot), True)

            # left
            id_full_stab_mirror = rs.MirrorObject(id_full_stab, (-10, 0, -10), (10, 0, 10), True)

            stab_export = rs.JoinSurfaces((id_full_stab, id_full_stab_mirror), True)
            Parts_foil_export["stab"] = stab_export

            # surface deletion
            rs.DeleteObject(id_stab)
            rs.DeleteObject(id_patch_stab)
            rs.DeleteObject(id_full_stab_0)
            rs.DeleteObject(id_patch_stab_bot)
            rs.DeleteObject(id_full_stab)
            rs.DeleteObject(id_full_stab_mirror)

        except:
            curve_stab = rs.DuplicateEdgeCurves(id_stab)  # array of strings
            id_patch_stab = rs.AddPlanarSrf((curve_stab[1]))  # array of strings
            id_full_stab = rs.JoinSurfaces((id_patch_stab[0], id_stab), True)

            id_full_stab_mirror = rs.MirrorObject(id_full_stab, (-10, 0, -10), (10, 0, 10), True)

            stab_export = rs.JoinSurfaces((id_full_stab, id_full_stab_mirror), True)
            Parts_foil_export["stab"] = stab_export

            # surface deletion
            rs.DeleteObject(id_stab)
            rs.DeleteObject(id_full_stab)
            rs.DeleteObject(id_full_stab_mirror)

    if "mast" in Parts_foil.keys():
        """ closed mast """
        id_mast = id_Parts_foil["mast"]
        try:
            curve_mast_0 = rs.DuplicateEdgeCurves(id_mast)  # array of strings  # 0 left, 1 bottom, 2 right, 3 top
            id_patch_mast = rs.AddEdgeSrf((curve_mast_0[0], curve_mast_0[2]))
            id_full_mast = rs.JoinSurfaces((id_patch_mast, id_mast), True)
            curve_mast = rs.DuplicateEdgeCurves(id_full_mast)
            id_patch_mast_top = rs.AddEdgeSrf((curve_mast[0], curve_mast[5]))
            id_patch_mast_bot = rs.AddEdgeSrf((curve_mast[2], curve_mast[4]))
            # array of strings  # 0 left, 1 bottom, 2 right, 3 top, 4 bottom trailing edge, 5 top trailing edge

            mast_export = rs.JoinSurfaces((id_full_mast, id_patch_mast_top, id_patch_mast_bot), True)
            Parts_foil_export["mast"] = mast_export

            # surface deletion
            rs.DeleteObject(id_mast)
            rs.DeleteObject(id_patch_mast)
            rs.DeleteObject(id_patch_mast_top)
            rs.DeleteObject(id_patch_mast_bot)
            rs.DeleteObject(id_full_mast)

        except:
            curve_mast = rs.DuplicateEdgeCurves(id_mast)  # array of strings
            id_patch_mast_bot = rs.AddPlanarSrf((curve_mast[1]))  # array of strings
            id_patch_mast_top = rs.AddPlanarSrf((curve_mast[2]))  # array of strings

            mast_export = rs.JoinSurfaces((id_patch_mast_bot, id_patch_mast_top, id_mast), True)
            Parts_foil_export["mast"] = mast_export

            # surface deletion
            rs.DeleteObject(id_mast)
            rs.DeleteObject(id_patch_mast_bot)
            rs.DeleteObject(id_patch_mast_top)

    if "fuselage" in Parts_foil.keys():
        """ closed fuselage """
        # front
        id_fuselagefront = id_Parts_foil["fuselage_front"]
        curve_fuselagefront = rs.DuplicateEdgeCurves(id_fuselagefront)
        id_patch_fuselagefront = rs.AddPlanarSrf((curve_fuselagefront[1]))
        id_full_fuselagefront = rs.JoinSurfaces((id_patch_fuselagefront, id_fuselagefront), True)

        # rear
        id_fuselagerear = id_Parts_foil["fuselage_rear"]
        curve_fuselagerear = rs.DuplicateEdgeCurves(id_fuselagerear)
        id_patch_fuselagerear = rs.AddPlanarSrf((curve_fuselagerear[1]))  # string
        id_full_fuselagerear = rs.JoinSurfaces((id_patch_fuselagerear, id_fuselagerear), True)

        fuselage_export = rs.JoinSurfaces((id_full_fuselagefront, id_full_fuselagerear), True)
        Parts_foil_export["fuselage"] = fuselage_export

        # surface deletion
        rs.DeleteObject(id_fuselagefront)
        rs.DeleteObject(id_patch_fuselagefront)
        rs.DeleteObject(id_full_fuselagefront)
        rs.DeleteObject(id_fuselagerear)
        rs.DeleteObject(id_patch_fuselagerear)
        rs.DeleteObject(id_full_fuselagerear)

    # curve deletion
    arrObjects = rs.AllObjects()
    for el in arrObjects:
        if not(rs.IsPolysurface(el)):
            rs.DeleteObject(str(el))

    # Clears, saves and exports
    for extension in foil.L_extension:
       SaveAsRhinoFile(extension,Parts_foil_export)
    ClearRhinoFile()
    ClearLayerRhinoFile()
    rs.DocumentModified(False)  # prevents a dialog box from popping when closing Rhino
    if foil.close_Rhino == 'yes':
        rs.Exit()
    