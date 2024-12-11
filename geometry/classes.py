import math
from typing import List

import matplotlib.pyplot as plt
import matplotlib.patches
import matplotlib.lines
import numpy as np
from geometry.constants import *


class Point2D:
    """
    Представляет точку в 2D пространстве.

    Args:
        x (float): X-координата точки.
        y (float): Y-координата точки.

    Methods:
        __init__(x=None, y=None): Инициализирует объект Point2D.
        calc_dist(other): Вычисляет расстояние между двумя точками.
        __sub__(self, other): Вычитает одну точку из другой.
        __pow__(self, power, modulo=None): Возвращает каждую координату в степень.
        __str__(self): Возвращает строковое представление точки.

    Returns:
        str: Строковое представление точки (x y).
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
    Представляет линию в 2D пространстве.

    Args:
        first_point (Point2D): Первый конец линии.
        second_point (Point2D): Второй конец линии.

    Methods:
        __init__(a=None, b=None): Инициализирует объект Line.
        get_length(): Вычисляет длину линии.
        plot(ax, targets): Рисует линию на объекте matplotlib Axes.

    Returns:
        None
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
    Представляет круг в 2D пространстве.

    Args:
        x (float): X-координата центра круга.
        y (float): Y-координата центра круга.
        r (float): Радиус круга.

    Methods:
        __init__(x, y, r): Инициализирует объект Circle.
        plot(ax): Рисует круг на объекте matplotlib Axes.
        __str__(self): Возвращает строковое представление круга.
        __eq__(self, other): Сравнивает два объекта Circle.
        point_on(point): Проверяет, лежит ли точка на окружности.

    Returns:
        str: Строковое представление круга (x y radius).
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

    def __eq__(self, other):
        if not isinstance(other, Circle):
            return False
        return self.center.x == other.center.x and self.center.y == other.center.y and self.radius == other.radius

    def point_on(self, point: Point2D):
        return abs(self.center.calc_dist(point) - self.radius) < EPS

class Arc:
    """
    Представляет дугу окружности в 2D пространстве.

    Args:
        first_point (Point2D): Первая точка дуги.
        second_point (Point2D): Вторая точка дуги.
        circle (Circle): Окружность, на которой лежит дуга.

    Methods:
        __init__(a, b, circle): Инициализирует объект Arc.
        get_length(): Вычисляет длину дуги.
        plot(ax, targets): Рисует дугу на объекте matplotlib Axes.

    Returns:
        float: Длина дуги или INF в случае ошибки вычисления.
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
    Представляет путь, состоящий из геометрических фигур.

    Args:
        figures (list): Список геометрических фигур в пути.

    Methods:
        __init__(figures=None): Инициализирует объект GPath.
        __add__(self, other): Добавляет другой путь к текущему.
        __iadd__(self, other): Добавляет фигуры к текущему пути.

    Returns:
        None
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

    Args:
        points (List[Point2D]): Список точек, определяющих вершины многоугольника.

    Methods:
        __init__(points: List[Point2D] = None): Инициализирует экземпляр Polygon.
        plot_(ax: plt.Axes): Отображает многоугольник
        point_on(point:Point2D): проверяет, лежит ли точка на сторонах многоульгольника
    """


    def __init__(self, points:List[Point2D] = None):
        self.vertexes = points

    def plot(self, ax: plt.Axes):
        points_coords = [(point.x,point.y) for point in self.vertexes]
        polygon = matplotlib.patches.Polygon(points_coords, fill=True, color= "green", closed= True)
        ax.add_patch(polygon)

    def point_on(self, point:Point2D):
        f = False
        for v in self.vertexes:
            if abs(v.x - point.x) < EPS and abs(v.y - point.y) < EPS:
                f = True
                break
        return f
    def __eq__(self, other):
        if not isinstance(other, Polygon):
            return False
        return self.vertexes == other.vertexes


class LineFunction:
    """
        Класс, представляющий линейную функцию (прямую).

        Args:
            a:Point2D: первая точка, принадлежащая прямой
            b:Point2D: вторая точка принадлежащая прямой
            a_coef, b_coef, c_coef: коэффициенты прямой

        Methods:
            __init__(a:Point2D = None, b:Point2D = None, a_coef = None, b_coef = None, c_coef = None): Инициализирует экземпляр LineFunction.
            substitute(p:Point2D): проверка, лежит ли точка на прямой
        """
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