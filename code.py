import numpy as np
import matplotlib.pyplot as plt


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def array_convert(self):
        return np.array([self.x, self.y])

    def linear(self):
        return f"Vector(x={self.x}, y={self.y})"


class Matrix:
    def __init__(self, a, b, c, d):
        self.matrix = np.array([[a, b], [c, d]])

    def transform(self, vector):
        result = self.matrix @ vector.array_convert()
        return Vector(result[0], result[1])

    def points_transform(self, points):
        transformed_points = self.matrix @ points.T
        return transformed_points.T

    def __repr__(self):
        return f"Matrix(\n{self.matrix[0, 0]} {self.matrix[0, 1]}\n{self.matrix[1, 0]} {self.matrix[1, 1]}\n)"


class Shape:
    def __init__(self, points):
        self.points = np.array(points)

    def transform(self, matrix):
        transformed_points = matrix.points_transform(self.points)
        return Shape(transformed_points)

    def plot(self, ax, **kwargs):
        points = np.vstack([self.points, self.points[0]])
        ax.plot(points[:, 0], points[:, 1], **kwargs)

    def __repr__(self):
        return f"Shape(points={self.points})"


if __name__ == "__main__":
    batman_points = np.array([[0, 0], [1, 0.2], [0.4, 1], [0.5, 0.4], [0, 0.8], [-0.5, 0.4], [-0.4, 1], [-1, 0.2], [0, 0]])
    batman_shape = Shape(batman_points)

    rotation_matrix = Matrix(0, -1, 1, 0)

    transformed_batman_shape = batman_shape.transform(rotation_matrix)

    fig, ax = plt.subplots()
    batman_shape.plot(ax, color='yellow', label='Initial shape')
    transformed_batman_shape.plot(ax, color='red', label='Transformed shape')
    ax.set_aspect('equal')
    ax.legend()
    plt.show()
