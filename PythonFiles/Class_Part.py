from abc import ABCMeta, abstractmethod
import rhinoscriptsyntax as rs
from Class_Foil import Foil



class Part:

    """ defines a part of the foil """

    def __init__(self, side='right'):
        # General dimensions of the foil
        # x is the axis of the foil along the fuselage (-x towards the nose)
        # z is the vertical axis of the foil (along the mast)
        # y is so that x, y, and z create an orthonormal global coordinate system
        self._D = Foil.D  # width of the upper part of the mast (x-axis)
        self._G = Foil.G  # width of the lower part of the mast (x-axis)
        self._C = Foil.C  # length of the upper part of the mast (z-axis)
        self._F = Foil.F  # length of the lower part of the mast (z-axis)
        self._B = Foil.B  # mast full length (z-axis)
        # front wing
        self._K = Foil.K  # wing total length (considering both sides, y axis)
        self._R = Foil.R  # root chord of the front wing (x-axis)
        self._S = Foil.S  # tip chord of the front wing (x-axis)
        self._P = Foil.P  # distance between the front wing and the mast (x-axis)
        # stabilizer
        self._M = Foil.M  # stabilizer semispan (y-axis)
        self._L = Foil.L  # root chord of the stabilizer (x-axis)
        self._T = Foil.T  # tip chord of the stabilizer (x-axis)
        self._O = Foil.O  # distance between the stabilizer and the mast (x-axis)
        # fuselage
        self._H = Foil.H  # fuselage thickness (z-axis)
        self._Q = Foil.Q  # length of the front part of the fuselage (x-axis)
        self._V = Foil.V  # length of the rear part of the fuselage (x-axis)
        self._J = Foil.J  # fuselage full length (x-axis)

        self.side = side
        self.loose_surf = 1
        self.apex = Foil.apex  # three-dimensional tuple that defines the spatial position of the origin, which is the location of the front wing leading edge at the root chord

    def reverse(self):
        """ Changes the direction where the part will be created (+y to -y for instance) """
        if self.side == 'left':
            self.side = 'right'
        else:
            self.side = 'left'
        return self

    def curve1cp(self,points,degree,knots,weights,segment_num):
        curve = rs.AddNurbsCurve(points, knots, degree, weights)  # curve from B-Spline definition --> n_knots = n_points + degree - 1, weights are assigned to their respective points
        list = rs.DivideCurve(curve,segment_num,create_points=False,return_points=True)
        rs.DeleteObject(curve)
        # makes a list ready for interpolation :
        List=[]
        for i in range(len(list)):
            List.append(list[i].Item[1])
        return List



class Abstract:
    
    """ every parts must contain those functions """
    
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def dihedral_function(self, epsilon):
        """ Dihedral angle evolution for the part """
        pass

    @abstractmethod
    def twist_function(self, epsilon):
        """ Twist angle evolution for the part """
        pass

    @abstractmethod
    def sweep_function(self, epsilon):
        """ Sweep angle evolution for the part """
        pass

    @abstractmethod
    def chord_function(self, epsilon):
        """ Chord length evolution for the part """
        pass

    @abstractmethod
    def airfoil_function(self, epsilon, LEPoint, ChordFunct, ChordFactor, DihedralFunct, TwistFunct):
        """ Variation of cross section as a function of epsilon """
        pass
