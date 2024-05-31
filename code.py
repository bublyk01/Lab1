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
    def __init__(self, angle_deg, scale, mirror_axis, rotate_axis=None, rotate_axis_degrees=0):
        self.angle_deg = angle_deg
        self.scale = scale
        self.mirror_axis = mirror_axis
        self.rotate_axis = rotate_axis
        self.rotate_axis_degrees = rotate_axis_degrees

        angle_rad = np.deg2rad(angle_deg)
        cos_angle = np.cos(angle_rad)
        sin_angle = np.sin(angle_rad)
        self.rotation_matrix = np.array([[cos_angle, -sin_angle], [sin_angle, cos_angle]])

        rotate_axis_rad = np.deg2rad(rotate_axis_degrees)
        if rotate_axis == 'x':
            self.rotate_axis_matrix = np.array([[1, 0], [0, np.cos(rotate_axis_rad)]])
        elif rotate_axis == 'y':
            self.rotate_axis_matrix = np.array([[np.cos(rotate_axis_rad), 0], [0, 1]])
        else:
            self.rotate_axis_matrix = np.eye(2)

        if mirror_axis == 'x':
            self.mirror_matrix = np.array([[1, 0], [0, -1]])
        elif mirror_axis == 'y':
            self.mirror_matrix = np.array([[-1, 0], [0, 1]])
        elif mirror_axis == 'none':
            self.mirror_matrix = np.eye(2)
        else:
            raise ValueError("Invalid mirror axis. Please choose 'x', 'y', or 'none'.")

        self.matrix = self.rotation_matrix @ self.mirror_matrix @ self.rotate_axis_matrix * scale

    def transform(self, vector):
        transformed_vector = self.matrix @ vector.array_convert()
        return Vector(transformed_vector[0], transformed_vector[1])

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

    degrees = float(input("Enter the angle of rotation for the figure itself (degrees): "))
    scale = float(input("Enter the scaling factor: "))
    mirror_axis = input("Enter the mirror axis ('x', 'y', or 'none'): ")
    rotate_axis = input("Enter the axis to rotate ('x', 'y', or 'none'): ")
    rotate_axis_degrees = float(input("Enter amount of degrees by which you want to rotate the chosen axis: "))

    transformation_matrix = Matrix(degrees, scale, mirror_axis, rotate_axis, rotate_axis_degrees)

    transformed_batman_shape = batman_shape.transform(transformation_matrix)

    fig, ax = plt.subplots()
    batman_shape.plot(ax, color='yellow', label='Original')
    transformed_batman_shape.plot(ax, color='red', linestyle='--', label='Transformed')
    ax.set_aspect('equal')
    ax.legend()
    plt.show()
