class Edge:
    
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __repr__(self) -> str:
        return f'Edge: a = {str(self.a)} b = {str(self.b)}'
