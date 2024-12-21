from math import pi
class Circle:
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return pi * self.radius * self.radius

    def perimeter(self):
        return 2 * self.radius * pi


radius = float(input("Enter the radius of circle: "))
circle = Circle(radius)
print(f"Area of circle: {circle.area()}")
print(f"Perimeter of circle: {circle.perimeter()}")
