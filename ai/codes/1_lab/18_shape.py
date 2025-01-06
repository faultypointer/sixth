from math import pi

class Shape:
    def area(self):
        return 0

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
        
    def area(self):
        return pi * self.radius * self.radius 

class Rectangle(Shape):
    def __init__(self, length, breadth):
        self.length = length
        self.breadth = breadth

    def area(self):
        return self.length * self.breadth


circ = Circle(2.3)
rect = Rectangle(3, 4)
print(f"Area of circle: {circ.area()}")
print(f"Area of rectangle: {rect.area()}")
