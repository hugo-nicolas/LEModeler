import math
import rhinoscriptsyntax as rs
from Class_Part import Part, Abstract
from Class_Foil import Foil
import primitives, airconics_setup, liftingsurface, AirCONICStools as act



class Wing(Part, Abstract):

    """ defines the front wing of the foil """

    def __init__(self):
        super(Wing, self).__init__()
        self._apex = (self.apex[0], self.apex[1], self.apex[2])
        self.dihedral_f = Foil.dw
        self.dihedral_scale = 1.0
        self.dihedral_weight = 3.0
        self.sweep_f = Foil.sw
        self.sweep_scale = 1.0
        self.sweep_weight = 1.0
        self.twist_s = Foil.tw
        self.twist_scale = 1.0
        self.twist_weight = 1.0
        self.aoa = Foil.aoaw
        self.taper_ratio = (Foil.S/Foil.R)
        self.chord_f = -1.0 * self.taper_ratio + 1.0
        self.chord_scale = 1.0
        self.segment_num = int(Foil.numsegw)
        
        # Line B-spline definition works as unity on x and unity on y, meaning introducing
        # a length leading edge scale, concerning the leading edge profile itself.

        # curve1cp is making a B-Spline wing with one control point between start and end of the line
        # (3 control point B_spline)

        """ Dihedral B-SPLINE definition """
        list_points_dihedral = self.curve1cp(((0.0, 0.0, 0.0), (0.75, .25 * self.dihedral_scale, 0.0), (1.0, 1 * self.dihedral_scale, 0.0)), 2, (1, 1, 2, 2), (1, self.dihedral_weight, 1), self.segment_num)
        self.Lpoints_dihedral = []
        for i in range(len(list_points_dihedral)):
            self.Lpoints_dihedral.append(self.dihedral_f / self.dihedral_scale * list_points_dihedral[i])

        """ Twist B-SPLINE definition """
        list_points_twist = self.curve1cp(((0.0, 0.0, 0.0), (0.2 * self.twist_scale, 0.7, 0.0), (1.0 * self.twist_scale, 1.0, 0.0)), 2, (1, 1, 2, 2), (1, self.twist_weight, 1), self.segment_num)
        self.Lpoints_twist = []
        for i in range(len(list_points_twist)):
            self.Lpoints_twist.append(self.twist_s / self.twist_scale * list_points_twist[i])

        """ Sweep B-SPLINE definition """
        list_points_sweep = self.curve1cp(((0.0, 0.0, 0.0), (0.7, 0.7 * self.sweep_scale, 0), (1, 1 * self.sweep_scale, 0.0)), 2, (1, 1, 2, 2), (1, self.sweep_weight, 1), self.segment_num)
        self.Lpoints_sweep = []
        for i in range(len(list_points_sweep)):
            self.Lpoints_sweep.append(self.sweep_f / self.sweep_scale * list_points_sweep[i])

        """ Chord B-SPLINE definition """
        # chord is originally dimensionless and is part of the final wing scaling
        list_points_chord = self.curve1cp(((0.0, 0.0, 0.0), (0.5, 0.5*self.chord_f, 0.0), (1.0, 1.0*self.chord_f, 0.0)), 2, (1, 1, 2, 2), (1, 1, 1), self.segment_num)
        self.Lpoints_chord = []
        for i in range(len(list_points_chord)):
            self.Lpoints_chord.append(self.chord_scale * list_points_chord[i])


    def get_Lpoints_dihedral(self):
        return self.Lpoints_dihedral

    def get_Lpoints_twist(self):
        return self.Lpoints_twist

    def get_Lpoints_sweep(self):
        return self.Lpoints_sweep

    def get_Lpoints_chord(self):
        return self.Lpoints_chord

    # before the following functions, everything is horizontal by default
    
    def dihedral_function(self, epsilon=0.0):
        """ Dihedral angle evolution for the wing """
        eps_array = []
        for i in range(0, self.segment_num + 1):  # 11 = numSegment + 1, numSegment along the span
            list.append(eps_array, float(i) / self.segment_num)  # 10 = numSegment, eps_array = abscissa for interpolating L_points_dihedral
        f = act.linear_interpolation(eps_array, self.Lpoints_dihedral)
        return f(epsilon)  # returns the function of the evolution of the dihedral angle

    def twist_function(self, epsilon=0.0):
        """ Twist angle evolution for the wing """
        eps_array = []
        for i in range(0, self.segment_num + 1):
            list.append(eps_array, float(i) / self.segment_num)
        f = act.linear_interpolation(eps_array, self.Lpoints_twist)
        return f(epsilon)  # returns the function of the evolution of the twist angle

    def sweep_function(self, epsilon=0.0):
        """ Sweep angle evolution for the wing """
        eps_array = []
        for i in range(0, self.segment_num + 1):
            list.append(eps_array, float(i) / self.segment_num)
        f = act.linear_interpolation(eps_array, self.Lpoints_sweep)
        return f(epsilon)  # returns the function of the evolution of the sweep angle

    def chord_function(self, epsilon=0.0):
        """ Chord length evolution for the wing """
        eps_array = []
        for i in range(0, self.segment_num + 1):
            list.append(eps_array, float(i) / self.segment_num)
        f = act.linear_interpolation(eps_array, self.Lpoints_chord)
        return 1 - f(epsilon)  # returns the function of the evolution of chord
        # the chord is maximum at the middle of the wing

    def airfoil_function(self, epsilon, LEPoint, ChordFunct, ChordFactor, DihedralFunct, TwistFunct):
        """ Variation of cross section as a function of epsilon """
        AirfoilChordLength = (ChordFactor * ChordFunct(epsilon)) / math.cos(math.radians(TwistFunct(epsilon)))
        Af = primitives.Airfoil(LEPoint, AirfoilChordLength, DihedralFunct(epsilon), TwistFunct(epsilon),
                                airconics_setup.SeligPath)
        Airf, Chrd, ChordLength = primitives.Airfoil.AddAirfoilFromSeligFile(Af, Foil.front_wing_section)
        rs.RotateObject(Airf, (1*ChordLength, 0, 0), -self.aoa, rs.VectorCreate((0, 0, 0), (0, 1, 0)))
        rs.RotateObject(Chrd, (1*ChordLength, 0, 0), -self.aoa, rs.VectorCreate((0, 0, 0), (0, 1, 0)))
        # imports the .dat file of the section to be used for the wing
        return Airf, Chrd

    def generate_wing(self):
        """ Generates the front wing """
        wing_wing = liftingsurface.LiftingSurface(self.side, self._apex, self.sweep_function,
                                                  self.dihedral_function, self.twist_function,
                                                  self.chord_function, self.airfoil_function, self.loose_surf,
                                                  self.segment_num, TipRequired=False)
        ChordFactor = self._R / (self._K)
        ScaleFactor = self._R / ChordFactor
        id = wing_wing.GenerateLiftingSurface(ChordFactor, ScaleFactor)[0]
        # creation of the front wing from the imported section
        return id
