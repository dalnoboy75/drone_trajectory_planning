import math
from typing import List

import matplotlib.pyplot as plt
import matplotlib.patches
import matplotlib.lines
import numpy as np

INF = 10 ** 8


class Point2D:
    """
        Класс представляющий точку в двумерном пространстве.

        Атрибуты:
        x (float): X-координата точки.
        y (float): Y-координата точки.

        Методы:
        __init__(x=None, y=None): Инициализирует объект Point2D.
        calc_dist(other): Вычисляет расстояние между текущей точкой и другой точкой.
        """

    def __init__(self, x=None, y=None):
        if x == y == None:
            self.x = self.y = None
        else:
            self.x = x
            self.y = y

    def calc_dist(self, other):
        return math.hypot(other.x - self.x, other.y - self.y)

    def __sub__(self, other):
        return Point2D(self.x - other.x, self.y - other.y)

    def __pow__(self, power, modulo=None):
        return (self.x ** power + self.y ** power)

    def __str__(self):
        return f'{self.x} {self.y}'


class Line:
    """
       Класс представляющий линию в двумерном пространстве.

       Атрибуты:
       first_point (Point2D): Первый конец линии.
       second_point (Point2D): Второй конец линии.

       Методы:
       __init__(a=None, b=None): Инициализирует объект Line.
       get_length(): Вычисляет длину линии.
       """

    def __init__(self, a: Point2D = None, b: Point2D = None):
        if a == b == None:
            self.first_point = self.second_point = None
        else:
            self.first_point = a
            self.second_point = b

    def get_length(self):
        return self.first_point.calc_dist(self.second_point)

    def plot(self, ax: plt.Axes, targets):
        # Рисуем линию
        l = matplotlib.lines.Line2D([self.first_point.x, self.second_point.x],
                                    [self.first_point.y, self.second_point.y], color="blue")
        if (self.first_point in targets):
            ax.scatter(self.first_point.x, self.first_point.y, color="black")
        else:
            ax.scatter(self.first_point.x, self.first_point.y, color="purple")
        if (self.second_point in targets):
            ax.scatter(self.second_point.x, self.second_point.y, color="black")
        else:
            ax.scatter(self.second_point.x, self.second_point.y, color="purple")
        ax.add_line(l)


class Circle:
    """
        Класс представляющий круг в двумерном пространстве.

        Атрибуты:
        center (Point2D): Центр круга.
        radius (float): Радиус круга.

        Методы:
        __init__(x, y, r): Инициализирует объект Circle.
        """
    center: Point2D

    def __init__(self, x, y, r):
        self.center = Point2D(x, y)
        self.radius = r

    def plot(self, ax: plt.Axes):
        ax.add_patch(
            matplotlib.patches.Circle((self.center.x, self.center.y), self.radius, fill=False, edgecolor='black',
                                      linewidth=0.5))

    def __str__(self):
        return f'Circle {self.center.x} {self.center.y} {self.radius}'

    def __cmp__(self, other):
        return self.center.x == other.center.x and self.center.y == other.center.y and self.radius == other.radius


class Arc:
    """
        Класс представляющий дугу окружности в двумерном пространстве.

        Атрибуты:
        first_point (Point2D): Первая точка дуги.
        second_point (Point2D): Вторая точка дуги.
        circle (Circle): Окружность, на которой лежит дуга.

        Методы:
        __init__(a, b, circle): Инициализирует объект Arc.
        get_length(): Вычисляет длину дуги.
        """

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

    def plot(self, ax: plt.Axes, targets):
        start_angle = np.degrees(
            np.arctan2(self.first_point.y - self.circle.center.y, self.first_point.x - self.circle.center.x))
        end_angle = np.degrees(
            np.arctan2(self.second_point.y - self.circle.center.y, self.second_point.x - self.circle.center.x))
        start_angle = (start_angle + 360) % 360
        end_angle = (end_angle + 360) % 360
        arc_patch = matplotlib.patches.Arc((self.circle.center.x, self.circle.center.y), 2 * self.circle.radius,
                                           2 * self.circle.radius,
                                           theta1=min(start_angle, end_angle),
                                           theta2=max(end_angle, start_angle), edgecolor="orange")
        ax.add_patch(arc_patch)


class GPath:
    """
        Класс представляющий путь в двумерном пространстве.

        Атрибуты:
        route (list): Список фигур, входящих в путь.

        Методы:
        __init__(figures=None): Инициализирует объект GPath.
        """

    def __init__(self, figures: list = None):
        if figures is None:
            self.route = list()
        else:
            self.route = figures

    def __add__(self, other):
        return GPath(self.route + other.route)

    def __iadd__(self, other):
        self.route += other.route
        return self

class Polygon:
    """
    Класс, представляющий многоугольник.

    Атрибуты:
        points (List[Point2D]): Список точек, определяющих вершины многоугольника.

    Методы:
        __init__(points: List[Point2D] = None):
            Инициализирует экземпляр Polygon.

            Аргументы:
                points (List[Point2D]): Список точек, определяющих вершины многоугольника.

        plot_(ax: plt.Axes):
            Отображает многоугольник

            Аргументы:
                ax (plt.Axes): Объект matplotlib Axes, на котором будет отображен многоугольник.
    """


    def __init__(self, points:List[Point2D] = None):
        self.vertexes = points

    def plot(self, ax: plt.Axes):
        points_coords = [(point.x,point.y) for point in self.vertexes]
        polygon = matplotlib.patches.Polygon(points_coords, fill=True, color= "green", closed= True)
        ax.add_patch(polygon)


class LineFunction:
    def __init__(self, a:Point2D = None, b:Point2D = None, a_coef = None, b_coef = None, c_coef = None):
        if (a is not None and b is not None):
            self.a = b.y - a.y
            self.b = -(b.x - a.x)
            self.c = -self.b* a.y - self.a * a.x
        else:
            self.a = a_coef
            self.b = b_coef
            self.c = c_coef
    def substitute(self, p:Point2D):
        return self.a * p.x + self.b * p.y + self.c