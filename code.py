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
