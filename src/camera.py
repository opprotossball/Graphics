from edge import Edge
import numpy as np

class Camera:

    def __init__(self, half_width: float, half_height: float, depth: float):
        self._half_width = half_width
        self._half_height = half_height
        self._view_center = np.array([0, 0, 0])
        self._x_rotation = np.identity(3, dtype=float)
        self._y_rotation = np.identity(3, dtype=float)
        self._z_rotation = np.identity(3, dtype=float)
        self._rotation = self.calculate_rotation()
        self._depth = depth
        self._focal_point = np.array([0, 0, -depth], dtype=float)

    # find intersection with viewing plane in camera space (d = 0)
    def plane_intersection(self, point):
        # -t = d / (d + z)
        nt = self._depth / (self._depth + point[2])
        # p' = (0 - tx, 0 - ty, -d - tz - td)
        return np.array([nt * point[0], nt * point[1], 0], dtype=float)

    def move(self, translation):
        self._view_center += translation


    def calculate_rotation(self):
        return self._x_rotation @ self._y_rotation @ self._z_rotation

    def scene_to_camera_space(self, point):
        return self._rotation @ point - self._view_center 
    
    def edge_to_camera_space(self, edge: Edge):
        a = self.scene_to_camera_space(edge.a)
        b = self.scene_to_camera_space(edge.b)
        # check if both ends are on the correct side of plane (a.z >= 0 && b.z >= 0) 
        if a[2] < 0 or b[2] < 0:
            return None
        ai = self.plane_intersection(a)
        # check if points fit in frame
        if abs(ai[0]) > self._half_width or abs(ai[1]) > self._half_height:
            return None 
        bi = self.plane_intersection(b)
        if abs(bi[0]) > self._half_width or abs(bi[1]) > self._half_height:
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
        return f'Camera\n    view_center: {self._view_center}\n    focal_point: {self._focal_point}\n    rotation: \n{self._rotation}\n'