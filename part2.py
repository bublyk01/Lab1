import numpy as np
import cv2

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def array_convert(self):
        return np.array([self.x, self.y])

class Matrix:
    def __init__(self, angle_deg=0, scale=1, mirror_axis='none', custom_matrix=None):
        if custom_matrix is not None:
            self.matrix = np.array(custom_matrix)
        else:
            angle_rad = np.deg2rad(angle_deg)
            cos_angle = np.cos(angle_rad)
            sin_angle = np.sin(angle_rad)
            rotation_matrix = np.array([[cos_angle, -sin_angle], [sin_angle, cos_angle]])

            mirror_matrix = np.eye(2)
            if mirror_axis == 'x':
                mirror_matrix = np.array([[1, 0], [0, -1]])
            elif mirror_axis == 'y':
                mirror_matrix = np.array([[-1, 0], [0, 1]])

            self.matrix = rotation_matrix @ mirror_matrix * scale

    def transform(self, vector):
        transformed_vector = self.matrix @ vector.array_convert()
        return Vector(transformed_vector[0], transformed_vector[1])

    def points_transform(self, points):
        return (self.matrix @ points.T).T

class Shape:
    def __init__(self, points):
        self.points = np.array(points)

    def transform(self, matrix):
        transformed_points = matrix.points_transform(self.points)
        return Shape(transformed_points)

    def plot(self, image, color, thickness):
        points = np.vstack([self.points, self.points[0]]).astype(np.int32)
        points[:, 0] += image.shape[1] // 2
        points[:, 1] = image.shape[0] // 2 - points[:, 1]
        cv2.polylines(image, [points], isClosed=True, color=color, thickness=thickness)

if __name__ == "__main__":
    batman_points = np.array([[0, 0], [100, 20], [40, 100], [50, 40], [0, 80], [-50, 40], [-40, 100], [-100, 20], [0, 0]])
    batman_shape = Shape(batman_points)

    choice = input("Do you want to enter your own transformation matrix? ").strip().lower()

    if choice == "yes":
        custom_matrix = []
        print("Enter your transformation matrix (2x2):")
        for i in range(2):
            row = list(map(float, input(f"Row {i + 1}: ").split()))
            if len(row) != 2:
                raise ValueError("Each row must have exactly 2 elements.")
            custom_matrix.append(row)
        transformation_matrix = Matrix(custom_matrix=custom_matrix)
    else:
        degrees = float(input("Enter the angle of rotation for the figure itself (degrees): "))
        scale = float(input("Enter the scaling factor: "))
        mirror_axis = input("Enter the mirror axis ('x', 'y', or 'none'): ")

        transformation_matrix = Matrix(degrees, scale, mirror_axis)

    transformed_batman_shape = batman_shape.transform(transformation_matrix)

    image = np.ones((500, 500, 3), dtype=np.uint8) * 255
    batman_shape.plot(image, color=(0, 255, 255), thickness=2)
    transformed_batman_shape.plot(image, color=(255, 0, 0), thickness=2)

    cv2.imshow(" Shape transformation result", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
