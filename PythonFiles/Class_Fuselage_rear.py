from Class_Part import Part, Abstract
from Class_Foil import Foil
import primitives, airconics_setup, liftingsurface



class Fuselagerear(Part, Abstract):

    """ defines the rear part of the fuselage of the foil """

    def __init__(self):
        super(Fuselagerear, self).__init__()
        self.chord_scale = 1.0
        self._apex = (self.apex[0], self.apex[1], self.apex[2])
        self.segment_num = int(10)
        
    # before the following functions, everything is horizontal by default
    
    def dihedral_function(self, epsilon=0.0):
        """ Dihedral angle evolution for the rear part of the fuselage """
        return 0  # degree

    def twist_function(self, epsilon=0.0):
        """ Twist angle evolution for the rear part of the fuselage """
        return -90  # degree

    def sweep_function(self, epsilon=0.0):
        """ Sweep angle evolution for the rear part of the fuselage """
        return 0  # degree

    def chord_function(self, epsilon=0.0):
        """ Chord length evolution for the rear part of the fuselage """
        return 1 - 0.5*epsilon  # the chord will decrease linearly

    def airfoil_function(self, epsilon, LEPoint, ChordFunct, ChordFactor, DihedralFunct, TwistFunct):
        """ Variation of cross section as a function of epsilon """
        AirfoilChordLength = (ChordFactor * ChordFunct(epsilon))
        Af = primitives.Airfoil(LEPoint, AirfoilChordLength, DihedralFunct(epsilon), TwistFunct(epsilon),
                                airconics_setup.SeligPath)  # parameters for the fuselage
        Airf, Chrd, ChordLength = primitives.Airfoil.AddAirfoilFromSeligFile(Af, Foil.fuselage_rear_section, "fuselage", 1)
        # imports the self-created section for the fuselage (.dat)
        return Airf, Chrd

    def generate_wing(self):
        """ Generates the rear part of the fuselage """
        fuselagerear_wing = liftingsurface.LiftingSurface(self.side, self._apex, self.sweep_function,
                                                  self.dihedral_function, self.twist_function,
                                                  self.chord_function, self.airfoil_function, self.loose_surf,
                                                  self.segment_num, TipRequired=False)
        ChordFactor = self._H / self._V  # of the fuselage's total length
        ScaleFactor = self._H / ChordFactor
        id = fuselagerear_wing.GenerateLiftingSurface(ChordFactor, ScaleFactor)[0]
        # creation of the rear part of the fuselage from the imported section
        return id
