from polygon_position import PolygonPosition
from sign import Sign

class BspNode:

    def __init__(self, polygons):
        self.front_child = None
        self.back_child = None
        if len(polygons) == 0:
            self.polygons = []
            return
        self.polygons = [polygons[0]]
        self.build(polygons[1:])

    def is_leaf(self):
        return self.front_child is None and self.back_child is None

    def build(self, polygons):
        front = []
        back = []
        for polygon in polygons:
            pos = self.polygons[0].others_relative_position(polygon)
            match pos:
                case PolygonPosition.BEHIND:
                    back.append(polygon)
                case PolygonPosition.ON_PLANE:
                    self.polygons.append(polygon)
                case PolygonPosition.IN_FRONT:
                    front.append(polygon)
                case PolygonPosition.INTERSECTS:
                    f, b = self.polygons[0].cut_other_polygon(polygon)
                    front.append(f)
                    back.append(b)
        # create empty child if not leaf
        if len(front) > 0 or len(back) > 0:
            self.front_child = BspNode(front)
            self.back_child = BspNode(back)
    
    def traverse(self, position, to_render):
        if self.is_leaf():
            for p in self.polygons:
                to_render.append(p)
            return
        point_sign = self.polygons[0].point_relative_sign(position)

        match point_sign:

            # view point in front
            case Sign.POSITIVE:
                self.back_child.traverse(position, to_render)
                for p in self.polygons:
                    to_render.append(p)
                self.front_child.traverse(position, to_render)

            # view point behind
            case Sign.NEGATIVE:
                self.front_child.traverse(position, to_render)
                for p in self.polygons:
                    to_render.append(p)
                self.back_child.traverse(position, to_render)

            # view point on plane
            case Sign.ZERO:
                self.front_child.traverse(position, to_render)
                self.back_child.traverse(position, to_render)

        return to_render
    
    def tst(self):
        print(len(self.polygons))
        for p in self.polygons:
            print(p.color, end=' ')
        print('\n')
        if self.is_leaf():
            return
        if self.front_child is not None:
            print("front")
            self.front_child.tst()
        if self.back_child is not None:
            print("back")
            self.back_child.tst()