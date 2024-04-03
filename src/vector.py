import numpy as np

class Vector:

    def __init__(self, *args):
        if len(args) == 0:
            self.pos = np.array([0, 0, 0], dtype=float)
        elif len(args) == 1 and isinstance(args[0], np.ndarray) and len(args[0] == 3):
            self.pos = args[0]
        elif len(args) == 3:
            self.pos = np.array(args, dtype=float)
        else:
            raise TypeError('Vector.__init__: Invalid parmeters given')
    
    @property
    def x(self):
        return self.pos[0]
    
    @property
    def y(self):
        return self.pos[1]
    
    @property
    def z(self):
        return self.pos[2]
    
    @x.setter
    def x(self, value):
        self.pos[0] = value
    
    @y.setter
    def y(self, value):
        self.pos[1] = value
    
    @z.setter
    def z(self, value):
        self.pos[2] = value

    def normalize(self):
        self.pos = self.pos / (self.pos**2).sum()**0.5

    def direction(self, other):
        return Vector(np.array(other.pos, copy=True) - self.pos).normalize()
    
    def __mul__(self, other):
        if isinstance(other, float):
            return Vector(self.pos * other)
        else:
            raise TypeError(f"unsupported operand type(s) for *: '{self.__class__}' and '{type(other)}'")
        
    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(self.pos + other.pos)
        else:
            raise TypeError(f"unsupported operand type(s) for +: '{self.__class__}' and '{type(other)}'")
        
    def __sub__(self, other):
        if isinstance(other, Vector):
            return Vector(self.pos - other.pos)
        else:
            raise TypeError(f"unsupported operand type(s) for -: '{self.__class__}' and '{type(other)}'")

    def __truediv__(self, other):
        pass

    def __repr__(self) -> str:
        return f'({self.x}, {self.y}, {self.z})'