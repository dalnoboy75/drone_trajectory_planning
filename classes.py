import math
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

    def plot(self, ax: plt.Axes):
        # Рисуем линию
        l = matplotlib.lines.Line2D([self.first_point.x, self.second_point.x],
                                    [self.first_point.y, self.second_point.y], color="blue")
        ax.scatter(self.first_point.x, self.first_point.y, color="purple")
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

    def __init__(self, x, y, r):
        self.center = Point2D(x, y)
        self.radius = r

    def plot(self, ax: plt.Axes):
        ax.add_patch(
            matplotlib.patches.Circle((self.center.x, self.center.y), self.radius, fill=False, edgecolor='black',
                                      linewidth=0.5))


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

    def plot(self, ax: plt.Axes):
        start_angle = np.degrees(
            np.arctan2(self.first_point.y - self.circle.center.y, self.first_point.x - self.circle.center.x))
        end_angle = np.degrees(
            np.arctan2(self.second_point.y - self.circle.center.y, self.second_point.x - self.circle.center.x))

        arc_patch = matplotlib.patches.Arc((self.circle.center.x, self.circle.center.y), 2 * self.circle.radius,
                                           2 * self.circle.radius,
                                           theta1=start_angle,
                                           theta2=end_angle, edgecolor="orange")
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
