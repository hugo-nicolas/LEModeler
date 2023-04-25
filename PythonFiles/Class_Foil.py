from Dimensions import foil_parameters



class Foil:

    """ defines the whole foil"""

    L_values, L_sections, L_extension, L_isSymmetric, L_closeRhino = foil_parameters()

    # General dimensions of the foil
    # x is the axis of the foil along the fuselage (-x towards the nose)
    # z is the vertical axis of the foil (along the mast)
    # y is so that x, y, and z create an orthonormal global coordinate system

    # please ensure that the following variables are floats, otherwise bugs may occur

    # mast
    D = L_values[0]  # width of the upper part of the mast (x-axis)
    G = L_values[1]  # width of the lower part of the mast (x-axis)
    C = L_values[2]  # length of the upper part of the mast (z-axis)
    F = L_values[3]  # length of the lower part of the mast (z-axis)
    B = float(C + F)  # mast full length (z-axis)
    # front wing
    K = L_values[4]  # front wing semispan (y-axis)
    R = L_values[5]  # root chord of the front wing (x-axis)
    S = L_values[6]  # tip chord of the front wing (x-axis)
    P = L_values[7]  # distance between the front wing and the mast (x-axis)
    # stabilizer
    M = L_values[8]  # stabilizer semispan (y-axis)
    L = L_values[9]  # root chord of the stabilizer (x-axis)
    T = L_values[10]  # tip chord of the stabilizer (x-axis)
    O = L_values[11]  # distance between the stabilizer and the mast (x-axis)
    # fuselage
    H = L_values[12]  # fuselage thickness (z-axis)
    Q = L_values[13]  # length of the front part of the fuselage (x-axis)
    V = L_values[14]  # length of the rear part of the fuselage (x-axis)
    J = float(V + Q)  # fuselage full length (x-axis)

    # Final bending angles (degree)
    # front wing
    dw = L_values[15]  # dihedral angle of the front wing
    sw = L_values[16]  # sweep angle of the front wing
    tw = L_values[17]  # twist angle of the front wing - please make sure that the front wing section fully stands within the fuselage
    aoaw = L_values[18]  # angle of attack of the front wing
    # stabilizer
    dbw = L_values[19]  # dihedral angle of the stabilizer
    sbw = L_values[20]  # sweep angle of the stabilizer
    tbw = L_values[21]  # twist angle of the stabilizer - please make sure that the stab section fully stands within the fuselage
    aoabw = L_values[22]  # angle of attack of the stabilizer

    # Number of segments
    # front wing
    numsegw = L_values[23]  # discretization along the front wing semispan
    # stabilizer
    numsegbw = L_values[24]  # discretization along the stabilizer semispan

    # Symmetry of the front wing
    symmetric = L_isSymmetric[0]  # boolean that defines whether the front wing is symmetric

    # Rhino closing
    close_Rhino = L_closeRhino[0]  # boolean that defines whether Rhino must be closed automatically

    # Sections
    mast_section = L_sections[0]
    front_wing_section = L_sections[1]
    stab_section = L_sections[2]
    fuselage_front_section = L_sections[3]
    fuselage_rear_section = L_sections[4]

    # Space coordinates to create the foil
    # three-dimensional tuple that defines the spatial position of the origin, which is the location of the front wing leading edge at the root chord
    apex = (0, 0, 0)


    def __init__(self, Parts_foil):  # Parts_foil = {"wing":wing,"stab":stab,"mast":mast,"fuselage":fuselage}
        if "wing" in Parts_foil.keys():
            self.wing = Parts_foil["wing"]  # list that contains the left and right part of the front wing
        if "stab" in Parts_foil.keys():
            self.stab = Parts_foil["stab"]  # list that contains the left and right part of the stabilizer
        if "mast" in Parts_foil.keys():
            self.mast = Parts_foil["mast"]
        if "fuselage" in Parts_foil.keys():
            self.fuselagefront = Parts_foil["fuselage"][0]
            if self.fuselagefront.side == 'right':
                self.fuselagefront.reverse()  # side becomes 'left' so that it goes along x
            self.fuselagerear = Parts_foil["fuselage"][1]
            if self.fuselagerear.side == 'left':
                self.fuselagerear.reverse()  # side becomes 'right' so that it goes along -x


    def make_foil(self, Parts_foil):
        """ Draws the whole foil under Rhinoceros """
        id_Parts_foil = dict()
        if "wing" in Parts_foil.keys():
            id_wing = self.wing.generate_wing()
            id_Parts_foil["wing"] = id_wing
        if "stab" in Parts_foil.keys():
            id_stab = self.stab.generate_wing()
            id_Parts_foil["stab"] = id_stab
        if "mast" in Parts_foil.keys():
            id_mast = self.mast.generate_wing()
            id_Parts_foil["mast"] = id_mast
        if "fuselage" in Parts_foil.keys():
            id_fuselagefront = self.fuselagefront.generate_wing()
            id_Parts_foil["fuselage_front"] = id_fuselagefront
            id_fuselagerear = self.fuselagerear.generate_wing()
            id_Parts_foil["fuselage_rear"] = id_fuselagerear
        return id_Parts_foil
