from edge import Edge
from vector import Vector
from utils import dot

class Camera:

    def __init__(self, half_width: float, half_height: float, depth: float, position: Vector, normal: Vector):
        self._half_width = half_width
        self._half_height = half_height
        self._depth = depth
        self._pos = position
        self._normal = normal
        self._view_center = self.calculate_view_center()
        self._d = self.calculate_d()

    def get_pos(self) -> Vector:
        return self._pos
    
    def set_pos(self, value: Vector) -> None:
        self._pos = value
        self.calculate_view_center()
        self.calculate_d()
    
    def calculate_view_center(self) -> float:
        return self._pos + (self._normal * self._depth)
    
    def calculate_d(self) -> float:
        # print('calc d: ', (self._view_center.x / self._normal.x == self._view_center.y / self._normal.y))
        # return self._view_center.x / self._normal.x 
        return 10.0

    def is_on_correct_side(self, point: Vector) -> bool:
        diff = point - self._view_center
        return dot(diff, self._normal) >= 0

    # find intersection with viewing plane in camera space (d = 0)
    def plane_intersection(self, point: Vector) -> Vector:
        ba = self._pos - point
        n_dot_a = dot(self._normal, point)
        n_dot_ba = dot(self._normal, ba)
        return point + (ba * ((self._d - n_dot_a) / n_dot_ba))

    def point_to_camera_space(self, point: Vector) -> Vector:
        print(point)
        res = point - self._view_center
        if res.z != 0:
            raise TypeError('Point not in viewing plane')
        return res
    
    def edge_to_camera_space(self, edge: Edge):
        # check if both ends are on the correct side of plane
        if not self.is_on_correct_side(edge.a) or not self.is_on_correct_side(edge.b):
            return None
        ai = self.point_to_camera_space(self.plane_intersection(edge.a))
        # check if point is in frame
        if abs(ai.x) > self._half_width or abs(ai.y) > self._half_height:
            return None 
        bi = self.point_to_camera_space(self.plane_intersection(edge.b))
        if abs(bi.x) > self._half_width or abs(bi.y) > self._half_height:
            return None
        return Edge(ai, bi)
    
    def shot_scene(self, scene: list[Edge]) -> list[Edge]:
        res = []
        for edge in scene:
            edge_in_camera = self.edge_to_camera_space(edge)
            if edge_in_camera is not None:
                res.append(edge_in_camera)
        return res

    def __repr__(self):
        return f'Camera\n    pos: {self._pos}\n    normal: {self._normal}\n    view_center: {self._view_center}\n    d: {self._d}'