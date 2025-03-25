import numpy as np
from math import sin, cos, radians
import uuid
from constants import CAMERA_DISTANCE


class Transformation:
    def __init__(self, transform_type, params=None):
        self.id = str(uuid.uuid4())[:8]
        self.type = transform_type
        self.params = params or {}
        self.matrix = np.identity(4)
        self.update_matrix()

    def update_matrix(self):
        if self.type == "scale":
            sx = float(self.params.get("x", 1.0))
            sy = float(self.params.get("y", 1.0))
            sz = float(self.params.get("z", 1.0))
            self.matrix = np.array(
                [[sx, 0, 0, 0], [0, sy, 0, 0], [0, 0, sz, 0], [0, 0, 0, 1]]
            )
        elif self.type == "rotate_x":
            angle = radians(float(self.params.get("angle", 0.0)))
            self.matrix = np.array(
                [
                    [1, 0, 0, 0],
                    [0, cos(angle), -sin(angle), 0],
                    [0, sin(angle), cos(angle), 0],
                    [0, 0, 0, 1],
                ]
            )
        elif self.type == "rotate_y":
            angle = radians(float(self.params.get("angle", 0.0)))
            self.matrix = np.array(
                [
                    [cos(angle), 0, sin(angle), 0],
                    [0, 1, 0, 0],
                    [-sin(angle), 0, cos(angle), 0],
                    [0, 0, 0, 1],
                ]
            )
        elif self.type == "rotate_z":
            angle = radians(float(self.params.get("angle", 0.0)))
            self.matrix = np.array(
                [
                    [cos(angle), -sin(angle), 0, 0],
                    [sin(angle), cos(angle), 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1],
                ]
            )
        elif self.type == "translate":
            tx = float(self.params.get("x", 0.0))
            ty = float(self.params.get("y", 0.0))
            tz = float(self.params.get("z", 0.0))
            self.matrix = np.array(
                [[1, 0, 0, tx], [0, 1, 0, ty], [0, 0, 1, tz], [0, 0, 0, 1]]
            )
        elif self.type == "shear":
            xy = float(self.params.get("xy", 0.0))
            xz = float(self.params.get("xz", 0.0))
            yx = float(self.params.get("yx", 0.0))
            yz = float(self.params.get("yz", 0.0))
            zx = float(self.params.get("zx", 0.0))
            zy = float(self.params.get("zy", 0.0))
            self.matrix = np.array(
                [[1, xy, xz, 0], [yx, 1, yz, 0], [zx, zy, 1, 0], [0, 0, 0, 1]]
            )

    def get_display_text(self):
        if self.type == "scale":
            return f"Scale ({self.params.get('x', 1.0)}, {self.params.get('y', 1.0)}, {self.params.get('z', 1.0)})"
        elif self.type.startswith("rotate"):
            axis = self.type.split("_")[1].upper()
            return f"Rotate {axis} ({self.params.get('angle', 0.0)}°)"
        elif self.type == "translate":
            return f"Translate ({self.params.get('x', 0.0)}, {self.params.get('y', 0.0)}, {self.params.get('z', 0.0)})"
        elif self.type == "shear":
            return f"Shear (various parameters)"
        return self.type


def project_point(point, camera_distance=CAMERA_DISTANCE):
    """Convert 3D point to 2D with perspective projection"""
    z = point[2] + camera_distance
    if z <= 0:
        z = 0.1
    x = point[0] * camera_distance / z
    y = point[1] * camera_distance / z
    return (x, y)


def transform_vertices(vertices, transformations):
    """Apply all transformations to vertices"""
    homogeneous_vertices = np.ones((vertices.shape[0], 4))
    homogeneous_vertices[:, :3] = vertices

    combined_matrix = np.identity(4)
    for transform in transformations:
        combined_matrix = np.dot(combined_matrix, transform.matrix)

    transformed = np.dot(homogeneous_vertices, combined_matrix.T)

    return transformed[:, :3]
