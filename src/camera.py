from edge import Edge
import numpy as np
from math import sin, cos 
from quaternion import Quaternion
import rotations

class Camera:

    def __init__(self, half_width: float, half_height: float, depth: float):
        self._half_width = half_width
        self._half_height = half_height
        self._view_center = np.array([0, 0, 0], dtype=float)
        self._depth = depth
        self._rotation = Quaternion()

    # find intersection with viewing plane in camera space
    def plane_intersection(self, point):
        t = self._depth / point[2]
        return t * point

    def move(self, translation):
        self._view_center += self.x_axis_in_scene() * translation[0] + self.y_axis_in_scene() * translation[1] + self.z_axis_in_scene() * translation[2]
    
    def x_rotation(self, angle):
        self._rotation *= rotations.axis_angle_to_quat(np.array([1, 0, 0], dtype=float), angle)

    def y_rotation(self, angle):
        self._rotation *= rotations.axis_angle_to_quat(np.array([0, 1, 0], dtype=float), angle)

    def z_rotation(self, angle):
        self._rotation *= rotations.axis_angle_to_quat(np.array([0, 0, 1], dtype=float), angle)

    def x_axis_in_scene(self):
        return rotations.quat_rotate(np.array([1, 0, 0], dtype=float), self._rotation)
    
    def y_axis_in_scene(self):
        return rotations.quat_rotate(np.array([0, 1, 0], dtype=float), self._rotation)
    
    def z_axis_in_scene(self):
        return rotations.quat_rotate(np.array([0, 0, 1], dtype=float), self._rotation)

    def scene_to_camera_space(self, point):
        diff = point - self._view_center
        xp = np.dot(diff, self.x_axis_in_scene())
        yp = np.dot(diff, self.y_axis_in_scene())
        zp = np.dot(diff, self.z_axis_in_scene())
        return np.array([xp, yp, zp], dtype=float)
    
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

    def camera_to_display_space(self, point, display_half_width, display_half_height):
        x = point[0] * display_half_width / self._half_width + display_half_width
        y = point[1] * display_half_height / self._half_height + display_half_height
        return x, y
