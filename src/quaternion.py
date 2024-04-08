import numpy as np

class Quaternion:
    
    def __init__(self, a=1.0, b=0.0, c=0.0, d=0.0):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
    
    def __mul__(self, other):
        if not isinstance(other, Quaternion):
            raise ValueError(f'Cannot multiplay Quaternion by {type(other)}')
        res = Quaternion()
        res.a = (self.a * other.a) - (self.b * other.b) - (self.c * other.c) - (self.d * other.d)
        res.b = (self.a * other.b) + (self.b * other.a) + (self.c * other.d) - (self.d * other.c)
        res.c = (self.a * other.c) - (self.b * other.d) + (self.c * other.a) + (self.d * other.b)
        res.d = (self.a * other.d) + (self.b * other.c) - (self.c * other.b) + (self.d * other.a)
        return res

    def inverse(self):
        self.b *= -1
        self.c *= -1
        self.d *= -1

    def inversed(self):
        return Quaternion(self.a, -self.b, -self.c, -self.d)

    def as_vec(self):
        return np.array([self.a, self.b, self.c, self.d])
    