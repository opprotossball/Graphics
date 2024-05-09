from bsp_node import BspNode

class BspTree:

    def __init__(self, polygons):
        self.root = BspNode(polygons)

    def traverse(self, position):
        return self.root.traverse(position, [])

    def tst(self):
        self.root.tst()