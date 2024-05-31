import numpy as np
import matplotlib.pyplot as plt


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def array_convert(self):
        return np.array([self.x, self.y])

    def __linear__(self):
        return f"Vector(x={self.x}, y={self.y})"


class Matrix:
    def __init__(self, a, b, c, d):
        self.matrix = np.array([[a, b], [c, d]])

    def transform(self, vector):
        result = self.matrix @ vector.to_array()
        return Vector(result[0], result[1])

    def points_transform(self, points):
        transformed_points = self.matrix @ points.T
        return transformed_points.T

    def __repr__(self):
        return f"Matrix(\n{self.matrix[0, 0]} {self.matrix[0, 1]}\n{self.matrix[1, 0]} {self.matrix[1, 1]}\n)"
