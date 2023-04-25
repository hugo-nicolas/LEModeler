from Class_Part import Part, Abstract
from Class_Foil import Foil
import primitives, airconics_setup, liftingsurface, AirCONICStools as act



class Fuselagefront(Part, Abstract):

    """ defines the front part of the fuselage of the foil """

    def __init__(self):
        super(Fuselagefront, self).__init__()
        self.chord_scale = 0.99
        self._apex = (self.apex[0], self.apex[1], -self._H+self.apex[2])
        self.segment_num = int(10)

        # Line B-spline definition works as unity on x and unity on y, meaning introducing
        # a length leading edge scale, concerning the leading edge profile itself.

        # curve1cp is making a B-Spline wing with one control point between start and end of the line
        # (3 control point B_spline)

        """ Chord B-SPLINE definition """
        # chord is originally dimensionless and is part of the final wing scaling
        list_points_chord = self.curve1cp(((0.0, 0.0, 0.0), (0.8 * self._Q, 0.5 * self.chord_scale, 0.0), (1.0 * self._Q, 1 * self.chord_scale, 0.0)), 2, (1, 1, 2, 2), (1, 1, 1), self.segment_num)
        self.Lpoints_chord = []
        for i in range(len(list_points_chord)):
            self.Lpoints_chord.append(list_points_chord[i])

    def get_Lpoints_chord(self):
        return self.Lpoints_chord

    # before the following functions, everything is horizontal by default
    
    def dihedral_function(self, epsilon=0.0):
        """ Dihedral angle evolution for the front part of the fuselage """
        return 0  # degree

    def twist_function(self, epsilon=0.0):
        """ Twist angle evolution for the front part of the fuselage """
        return 90  # degree

    def sweep_function(self, epsilon=0.0):
        """ Sweep angle evolution for the front part of the fuselage """
        return 0  # degree

    def chord_function(self, epsilon=0.0):
        """ Chord length evolution for the front part of the fuselage """
        eps_array = []
        for i in range(0, self.segment_num + 1):
            list.append(eps_array, float(i) / self.segment_num)
        f = act.linear_interpolation(eps_array, self.Lpoints_chord)
        return 1 - (f(epsilon))**2.  # the chord will decrease in order to create the leading edge of the fuselage (nose)

    def airfoil_function(self, epsilon, LEPoint, ChordFunct, ChordFactor, DihedralFunct, TwistFunct):
        """ Variation of cross section as a function of epsilon """
        AirfoilChordLength = (ChordFactor * ChordFunct(epsilon))
        Af = primitives.Airfoil(LEPoint, AirfoilChordLength, DihedralFunct(epsilon), TwistFunct(epsilon),
                                airconics_setup.SeligPath)  # parameters for the fuselage
        print(self.__class__.__name__)
        Airf, Chrd, ChordLength = primitives.Airfoil.AddAirfoilFromSeligFile(Af, Foil.fuselage_front_section, "fuselage", 1)
        # imports the self-created section for the fuselage (.dat)
        return Airf, Chrd

    def generate_wing(self):
        """ Generates the front part of the fuselage """
        fuselagefront_wing = liftingsurface.LiftingSurface(self.side, self._apex, self.sweep_function,
                                                  self.dihedral_function, self.twist_function,
                                                  self.chord_function, self.airfoil_function, self.loose_surf,
                                                  self.segment_num, TipRequired=False)
        ChordFactor = self._H / self._Q  # of the fuselage's total length
        ScaleFactor = self._H / ChordFactor
        id = fuselagefront_wing.GenerateLiftingSurface(ChordFactor, ScaleFactor)[0]
        # creation of the front part of the fuselage from the imported section
        return id
        