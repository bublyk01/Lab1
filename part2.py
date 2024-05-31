import numpy as np
import cv2

class Matrix:
    def __init__(self, angle_deg=0, scale=1, mirror_axis='none', custom_matrix=None):
        if custom_matrix is not None:
            self.matrix = np.hstack([custom_matrix, np.array([[0], [0]])])
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

    def transform(self, image):
        rows, cols = image.shape[:2]
        return cv2.warpAffine(image, self.matrix, (cols, rows))

if __name__ == "__main__":
    # Load the image
    image = cv2.imread('image.jpg')

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
        degrees = float(input("Enter the angle of rotation for the image itself (degrees): "))
        scale = float(input("Enter the scaling factor: "))
        mirror_axis = input("Enter the mirror axis ('x', 'y', or 'none'): ")

        transformation_matrix = Matrix(degrees, scale, mirror_axis)

    transformed_image = transformation_matrix.transform(image)

    cv2.imshow("Transformed Image", transformed_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
