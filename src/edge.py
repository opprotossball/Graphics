from vector import Vector

class Edge:
    
    def __init__(self, a: Vector, b: Vector):
        self.a = a
        self.b = b

    def __repr__(self) -> str:
        return f'Edge: a = {str(self.a)} b = {str(self.b)}'
