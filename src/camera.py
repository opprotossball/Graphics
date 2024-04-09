from edge import Edge
import numpy as np
from quaternion import Quaternion
import rotations

class Camera:

    def __init__(self, half_width: float, half_height: float, depth: float, min_depth=1e-5, max_depth=1e5):
        self.half_width = half_width
        self.half_height = half_height
        self._view_center = np.array([0, 0, 0], dtype=float)
        self._depth = depth
        self._min_depth = min_depth
        self._max_depth = max_depth
        self._rotation = Quaternion()

    # find intersection with viewing plane in camera space
    def plane_intersection(self, point):
        t = self._depth / point[2]
        return t * point

    def move(self, translation):
        self._view_center += self.x_axis() * translation[0] + self.y_axis() * translation[1] + self.z_axis() * translation[2]
    
    def rotate_x(self, angle):
        self._rotation *= rotations.axis_angle_to_quat(np.array([1, 0, 0], dtype=float), angle)

    def rotate_y(self, angle):
        self._rotation *= rotations.axis_angle_to_quat(np.array([0, 1, 0], dtype=float), angle)

    def rotate_z(self, angle):
        self._rotation *= rotations.axis_angle_to_quat(np.array([0, 0, 1], dtype=float), angle)

    def x_axis(self):
        return rotations.quat_rotate(np.array([1, 0, 0], dtype=float), self._rotation)
    
    def y_axis(self):
        return rotations.quat_rotate(np.array([0, 1, 0], dtype=float), self._rotation)
    
    def z_axis(self):
        return rotations.quat_rotate(np.array([0, 0, 1], dtype=float), self._rotation)

    def zoom(self, delta):
        self._depth += delta
        self._depth = min(self._depth, self._max_depth)
        self._depth = max(self._depth, self._min_depth)

    def scene_to_camera_space(self, point):
        diff = point - self._view_center
        axes = np.array([self.x_axis(), self.y_axis(), self.z_axis()])
        return diff @ axes.T
    
    def edge_to_camera_space(self, edge: Edge):
        a = self.scene_to_camera_space(edge.a)
        b = self.scene_to_camera_space(edge.b)
        # check if both ends are on the correct side of plane 
        if a[2] <= self._depth or b[2] <= self._depth:
            return None
        ai = self.plane_intersection(a)
        bi = self.plane_intersection(b)
        return Edge(ai, bi)
    
    def shot_scene(self, scene: list[Edge]) -> list[Edge]:
        res = []
        for edge in scene:
            edge_in_camera = self.edge_to_camera_space(edge)
            if edge_in_camera is not None:
                res.append(edge_in_camera)
        return res

    def in_view(self, point) -> bool:
        return abs(point[0]) < self.half_width and abs(point[1]) < self.half_height

    def camera_to_display_space(self, point, display_half_width, display_half_height):
        x = point[0] * display_half_width / self.half_width + display_half_width
        y = point[1] * display_half_height / self.half_height + display_half_height
        return x, y
