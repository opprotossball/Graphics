import numpy as np
from sign import sign, Sign
from polygon_position import PolygonPosition
eps = 1e-5

class Polygon:

    def __init__(self, vertices, color=(255, 255, 255)):
        self.vertices = vertices
        self.color = color
        if not self.validate():
            pass
    
    def validate(self):
        n = len(self.vertices)
        if n < 3:
            return False
        
        # Finding a valid normal vector
        found = False
        for i in range(1, n-1):
            normal = np.cross(self.vertices[i] - self.vertices[0], self.vertices[i+1] - self.vertices[0])
            if np.linalg.norm(normal) > eps:
                found = True
                break
        if not found:
            # All points are collinear
            return False  
        
        # Check all points are in the same plane defined by the normal vector
        self.normal = normal / np.linalg.norm(normal)
        self.d = -np.dot(self.normal, self.vertices[0])
        for vertex in self.vertices:
            diff = np.dot(self.normal, vertex) + self.d
            if abs(diff) > eps:
                print(f"Non-coplanar point: {vertex}, Distance: {diff}")
                return False
        return True

    def others_relative_position(self, other):
        first_sign = self.point_relative_sign(other.vertices[0])

        for v in other.vertices[1:]:
            next_sign = self.point_relative_sign(v)
            if next_sign != first_sign:
                if first_sign != Sign.ZERO and next_sign != Sign.ZERO:
                    return PolygonPosition.INTERSECTS
                elif first_sign == Sign.ZERO:
                    first_sign = next_sign 
                    
        match first_sign:
            case Sign.NEGATIVE:
                return PolygonPosition.BEHIND
            case Sign.ZERO:
                return PolygonPosition.ON_PLANE
            case Sign.POSITIVE:
                return PolygonPosition.IN_FRONT

    def cut_other_polygon(self, other):
        front = []
        back = []
        for i in range(len(other.vertices)):
            v1 = other.vertices[i - 1]
            v2 = other.vertices[i]
            sign1 = self.point_relative_sign(v1)
            sign2 = self.point_relative_sign(v2)
            # if section is lying on plane treat it as lying in front
            if sign1 == Sign.ZERO and sign2 == Sign.ZERO:
                sign1 = Sign.POSITIVE
                sign2 = Sign.POSITIVE
            # treat ZERO as lying on same side
            if sign1 != sign2:
                if sign1 == Sign.ZERO:
                    sign1 = sign2
                elif sign2 == Sign.ZERO:
                    sign2 = sign1
            # same side
            if sign1 == sign2:
                if sign1 == Sign.POSITIVE:
                    front.append(v1)
                    front.append(v2)
                else:
                    back.append(v1)
                    back.append(v2)
            # different sides
            else:
                pass

    def point_relative_sign(self, point):
        return sign(np.dot(self.normal, point) + self.d)
    