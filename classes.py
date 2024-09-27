import math

INF = 10 ** 8


class Point2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def calc_dist(self, other):
        return math.hypot(other.x - self.x, other.y - self.y)


class Line:
    def __init__(self, a: Point2D, b: Point2D):
        self.first_point = a
        self.second_point = b

    def get_length(self):
        return self.first_point.calc_dist(self.second_point)


class Circle:
    def __init__(self, x, y, r):
        self.center = Point2D(x, y)
        self.radius = r


class Arc:
    def __init__(self, a: Point2D, b: Point2D, circle: Circle):
        self.first_point = a
        self.second_point = b
        self.circle = circle

    def get_length(self):
        chord = self.first_point.calc_dist(self.second_point)
        try:
            angle = math.acos((2 * self.circle.radius ** 2 - chord ** 2) / (2 * self.circle.radius ** 2))
        except:
            return INF
        return angle * self.circle.radius
