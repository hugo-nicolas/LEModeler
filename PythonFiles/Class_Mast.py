import math
from Class_Part import Part, Abstract
from Class_Foil import Foil
import primitives, liftingsurface



class Mast(Part, Abstract):

    """ defines the mast of the foil """

    def __init__(self):
        super(Mast, self).__init__()
        self._apex = (self.apex[0] + self._P, self.apex[1], self._B+self.apex[2])
        self.segment_num = int(15)

    # before the following functions, everything is horizontal by default
    
    def dihedral_function(self, epsilon=0.0):
        """ Dihedral angle evolution for the mast """
        return -90  # -90 is so that the mast is vertical

    def twist_function(self, epsilon=0.0):
        """ Twist angle evolution for the mast """
        # the twist is a function of the leading edge coordinates
        RootTwist = 0
        TipTwist = 0
        return RootTwist + epsilon * TipTwist

    def sweep_function(self, epsilon=0.0):
        """ Sweep angle evolution for the mast """
        return 0

    def chord_function(self, epsilon=0.0):
        """ Chord length evolution for the mast """
        if epsilon * self._B < self._C:
            return self._D / self._G
        elif epsilon * self._B > self._F:
            return 1
        else:
            return (self._D + (epsilon * self._B - self._C) * (self._G - self._D) / (self._F - self._C)) / self._G

    def airfoil_function(self, epsilon, LEPoint, ChordFunct, ChordFactor, DihedralFunct, TwistFunct):
        """ Variation of cross section as a function of epsilon """
        AirfoilChordLength = (ChordFactor * ChordFunct(epsilon)) / math.cos(math.radians(TwistFunct(epsilon)))
        Af = primitives.Airfoil(LEPoint, AirfoilChordLength, DihedralFunct(epsilon), TwistFunct(epsilon))
        SmoothingPasses = 1
        Airf, Chrd, ChordLength = primitives.Airfoil.AddAirfoilFromSeligFile(Af, Foil.mast_section)
        return Airf, Chrd

    def generate_wing(self):
        """ Generates the mast """
        mast_wing = liftingsurface.LiftingSurface(self.side, self._apex, self.sweep_function,
                                                  self.dihedral_function, self.twist_function,
                                                  self.chord_function, self.airfoil_function, self.loose_surf,
                                                  self.segment_num, TipRequired=False)
        ChordFactor = self._G / self._B
        ScaleFactor = self._G / (self._G/self._B)
        id = mast_wing.GenerateLiftingSurface(ChordFactor, ScaleFactor)[0]    
        return id
        