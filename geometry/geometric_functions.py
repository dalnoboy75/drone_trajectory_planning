from math import *
from typing import Union

from geometry import classes
from geometry.classes import *
from geometry.constants import *


# Расчёт количества точек пересечения с окружностью
def circle_intersection(a: classes.Point2D, b: classes.Point2D, circle: classes.Circle):
    """
        Проверяет, пересекается ли линия, проходящая через две точки, с кругом.

        Args:
            a (classes.Point2D): Первая точка линии
            b (classes.Point2D): Вторая точка линии
            circle (classes.Circle): Круг для проверки пересечения

        Returns:
            bool: True, если линия пересекает круг, False в противном случае
        """
    ax, ay = a.x, a.y
    bx, by = b.x, b.y
    ox, oy, r = circle.center.x, circle.center.y, circle.radius

    # Считаем коэф-ты кв. уравнения
    aa = (bx - ax) ** 2 + (by - ay) ** 2
    bb = (ax - ox) * (bx - ax) + (ay - oy) * (by - ay)
    cc = (ax - ox) ** 2 + (ay - oy) ** 2 - r ** 2

    d = bb ** 2 - aa * cc
    if 0 < d < EPS:
        d = 0
    if d > 0:
        return True
    else:
        return False


def polygon_intersection(a: classes.Point2D, b: classes.Point2D, polygon: classes.Polygon):
    """
        Проверяет, пересекается ли линия, проходящая через две точки, с многоугольником.

        Args:
            a (classes.Point2D): Первая точка линии
            b (classes.Point2D): Вторая точка линии
            polygon (classes.Polygon): Многоугольник для проверки пересечения

        Returns:
            bool: True, если линия пересекает многоугольник, False в противном случае
        """
    line = classes.LineFunction(a, b)
    vertexes = polygon.vertexes
    for i in range(len(vertexes)):
        v = classes.LineFunction(vertexes[i], vertexes[(i + 1) % len(vertexes)])
        if line.substitute(vertexes[i]) * line.substitute(vertexes[(i + 1) % len(vertexes)]) < -EPS and v.substitute(
                a) * v.substitute(b) < -EPS:
            return True

    pr = INF
    for i in range(len(vertexes)):
        if abs(line.substitute(vertexes[i])) <= EPS:
            if (pr + 1) % INF == 0 or i - pr == 1 or (pr == INF and i == 0) or i - pr == len(vertexes) - 1:
                pr = i
            else:
                return True
    return False


def intersection(a: Point2D, b: Point2D, object: Union[Circle, Polygon]):
    """
        Определяет тип объекта для проверки пересечения.

        Args:
            a (Point2D): Первая точка
            b (Point2D): Вторая точка
            object (Union[Circle, Polygon]): Объект для проверки пересечения (круг или многоугольник)

        Returns:
            bool: Результат проверки пересечения
        """
    if isinstance(object, classes.Circle):
        return circle_intersection(a, b, object)
    else:
        return polygon_intersection(a, b, object)


# Поиск точек касания касательных от точки с окружностью
def touch_points_search(point: classes.Point2D, object: Union[classes.Circle, classes.Polygon]):
    """
        Поиск точек касания между точкой и объектом.

        Args:
            point (Point2D): Точка для поиска касаний
            object (Union[Circle, Polygon]): Объект для определения касания (круг или многоугольник)

        Returns:
            Tuple[Point2D, Point2D] : Пара точек касания
            """
    if isinstance(object, classes.Circle):
        return circle_touch_points(point, object)
    elif isinstance(object, classes.Polygon):
        return polygon_touch_points(point, object)


def circle_touch_points(point: classes.Point2D, circle: classes.Circle):
    """
        Находит точки касания касательной от точки до круга.

        Args:
            point (classes.Point2D): Точка для определения касания
            circle (classes.Circle): Круг

        Returns:
            list: Список точек касания
        """
    lx = circle.center.x - point.x
    ly = circle.center.y - point.y
    l = sqrt(lx ** 2 + ly ** 2)
    r = circle.radius
    d = atan2(ly, lx)
    t = asin(r / l)
    t1x = r * sin(d - t) + circle.center.x
    t1y = r * (-cos(d - t)) + circle.center.y
    t2x = r * (-sin(d + t)) + circle.center.x
    t2y = r * cos(d + t) + circle.center.y

    return [classes.Point2D(round(t1x, ROUND_NUM), round(t1y, ROUND_NUM)),
            classes.Point2D(round(t2x, ROUND_NUM), round(t2y, ROUND_NUM))]


def polygon_touch_points(point: classes.Point2D, polygon: classes.Polygon):
    """
        Находит точки касания касательной от точки до многоугольника.

        Args:
            point (classes.Point2D): Точка для определения касания
            polygon (classes.Polygon): Многоугольник

        Returns:
            tuple: Две точки касания
        """
    center = Point2D(0, 0)
    vertexes = polygon.vertexes
    for ver in vertexes:
        center.x += ver.x
        center.y += ver.y
    center.x /= len(vertexes)
    center.y /= len(vertexes)

    tp1 = vertexes[0]
    tp2 = Point2D()
    cos_alpha_1 = 1.0
    cos_alpha_2 = 1.0
    center_dist = calc_dist(center, point)
    line = classes.LineFunction(center, point)

    for vertex in vertexes:
        if (line.substitute(vertex) * line.substitute(tp1)) < 0:
            tp2 = vertex
            break

    for vertex in vertexes:
        vertex_dist = calc_dist(vertex, point)
        center_vertex_dist = calc_dist(center, vertex)
        new_cos_alpha = (vertex_dist ** 2 + center_dist ** 2 - center_vertex_dist ** 2) / (
                2 * vertex_dist * center_dist)
        if line.substitute(vertex) * line.substitute(tp1) > 0 and new_cos_alpha < cos_alpha_1:
            cos_alpha_1 = new_cos_alpha
            tp1 = vertex
        if line.substitute(vertex) * line.substitute(tp2) > 0 and new_cos_alpha < cos_alpha_2:
            cos_alpha_2 = new_cos_alpha
            tp2 = vertex
    return tp1, tp2


# Расчёт расстояния между двумя точками
def calc_dist(first_point: classes.Point2D, second_point: classes.Point2D):
    """
        Вычисляет расстояние между двумя точками в двумерном пространстве.

        Args:
            first_point (classes.Point2D): Первая точка
            second_point (classes.Point2D): Вторая точка

        Returns:
            float: Расстояние между точками
            """
    return hypot(first_point.x - second_point.x, first_point.y - second_point.y)


# Расчёт длины дуги между двумя точками на окружности
def arc_length(first_point: classes.Point2D, second_point: classes.Point2D, circle: classes.Circle):
    """
        Вычисляет длину дуги между двумя точками на окружности.

        Args:
            first_point (classes.Point2D): Первая точка на окружности
            second_point (classes.Point2D): Вторая точка на окружности
            circle (classes.Circle): Окружность

        Returns:
            float: Длина дуги между точками
            """
    chord = calc_dist(first_point, second_point)
    try:
        angle = acos((2 * circle.radius ** 2 - chord ** 2) / (2 * circle.radius ** 2))
    except:
        return INF
    return angle * circle.radius


def tangents_between_circles(circle1: classes.Circle, circle2: classes.Circle):
    """
        Нахождение прямых касательных между двумя кругами.

        Args:
            circle1 (classes.Circle): Первый круг
            circle2 (classes.Circle): Второй круг

        Returns:
            list: Список линий касательных
            """
    tangents = []
    x0 = circle1.center.x
    y0 = circle1.center.y
    x1 = circle2.center.x
    y1 = circle2.center.y
    r0 = circle1.radius
    r1 = circle2.radius

    def find_tangent(r_0, r_1):
        a = None
        b = None
        c = None
        if abs(x0 - x1) > EPS:
            root = (x1 - x0) ** 2 * ((x1 - x0) ** 2 + (y1 - y0) ** 2 - (r_1 - r_0) ** 2)
            if abs(root) < EPS:
                root = 0
            else:
                root = sqrt(root)
            b = ((r_1 - r_0) * (y1 - y0) + root) / ((x1 - x0) ** 2 + (y1 - y0) ** 2)
            a = ((r_1 - r_0) - b * (y1 - y0)) / (x1 - x0)
            c = r_0 - a * x0 - b * y0
        else:
            a = abs(y1 - y0) / sqrt((r_1 - r_0) ** 2 + (y1 - y0) ** 2)
            b = (r_1 - r_0) / sqrt((r_1 - r_0) ** 2 + (y1 - y0) ** 2)
            c = r_0 - a * x0 - b * y0
        return LineFunction(a_coef=a, b_coef=b, c_coef=c)

    for n1 in [-1, 1]:
        for n2 in [-1, 1]:
            t = find_tangent(r0 * n1, r1 * n2)
            is_unique = t.a is not None
            if t in tangents:
                is_unique = False
            if is_unique:
                tangents.append(t)
    return tangents


def tangent_points(tangent: LineFunction, object1: Union[Circle, Polygon], object2: Union[Circle, Polygon]):
    """
        Находит точки касания касательной между двумя объектами.

        Args:
            tangent (LineFunction): Касательная
            object1 (Union[Circle, Polygon]): Объект для определения касания (круг или многоугольник)
            object2 (Union[Circle, Polygon]): Объект для определения касания (круг или многоугольник)
        Returns:
            List[Point2D]: Список точек касания
    """
    if isinstance(object1, Circle) and isinstance(object2, Circle):
        return tangent_points_circles(tangent, object1, object2)
    elif isinstance(object1, Polygon) and isinstance(object2, Polygon):
        return tangent_points_polygons(tangent, object1, object2)
    else:
        if isinstance(object1, Polygon):
            return tangent_points_polygon_circle(tangent, object1, object2)
        else:
            return tangent_points_polygon_circle(tangent, object2, object1)


def tangent_points_circles(tangent: LineFunction, circle1: classes.Circle, circle2: classes.Circle):
    """
        Находит точки пересечения линии касательной с двумя кругами.

        Args:
            tangent (LineFunction): Линия касательная
            circle1 (classes.Circle): Первый круг
            circle2 (classes.Circle): Второй круг

        Returns:
            tuple: Две точки пересечения
            """
    a, b, c = tangent.a, tangent.b, tangent.c
    x0 = circle1.center.x
    x1 = circle2.center.x
    y0 = circle1.center.y
    y1 = circle2.center.y
    r0 = circle1.radius
    r1 = circle2.radius

    p1_x = (x0 * b ** 2 - (a * (c + y0 * b))) / (a ** 2 + b ** 2)
    p2_x = (x1 * b ** 2 - (a * (c + y1 * b))) / (a ** 2 + b ** 2)

    p1_y = y0
    p2_y = y1
    if abs(b) > EPS:
        p1_y = a / b * (-p1_x) - c / b
        p2_y = a / b * (-p2_x) - c / b
    return classes.Point2D(p1_x, p1_y), classes.Point2D(p2_x, p2_y)


def dist_between_poly_points(a: classes.Point2D, b: classes.Point2D, polygon: classes.Polygon):
    """
        Вычисляет расстояние между двумя точками внутри многоугольника.

        Args:
            a (classes.Point2D): Первая точка
            b (classes.Point2D): Вторая точка
            polygon (classes.Polygon): Многоугольник

        Returns:
            tuple: Два значения:
                float: Расстояние между точками
                GPath: Путь, представляющий линию между точками
                """
    vertexes = polygon.vertexes
    v1 = None
    v2 = None
    for i, v in enumerate(vertexes):
        if abs(a.x - v.x) < EPS and abs(a.y - v.y) < EPS:
            v1 = i
    for i, v in enumerate(vertexes):
        if abs(b.x - v.x) < EPS and abs(b.y - v.y) < EPS:
            v2 = i
    if v2 < v1:
        v1, v2 = v2, v1
    path = GPath()
    points1 = vertexes[v1: v2 + 1]
    points2 = vertexes[v2:] + vertexes[:v1 + 1]

    def total_dist(points: list):
        dist = 0
        for i in range(len(points) - 1):
            dist += calc_dist(points[i], points[i + 1])
        return dist

    dist1 = total_dist(points1)
    dist2 = total_dist(points2)

    def points_to_path(points: list):
        path = GPath()
        for i in range(len(points) - 1):
            tpath = GPath([Line(points[i], points[i + 1])])
            path += tpath
        return path

    if dist1 < dist2:
        return dist1, points_to_path(points1)
    else:
        return dist2, points_to_path(points2)


def tangents_between_polygon(polygon: Polygon, obj: Union[Polygon, Circle]):
    """
        Нахождение линий касательных между многоугольником и другим объектом.

        Args:
            polygon (Polygon): Многоугольник
            obj (Union[Polygon, Circle]): Другой объект (многоугольник или круг)

        Returns:
            list: Список линий касательных
        """
    tangents = []
    vertexes = polygon.vertexes
    for vertex in vertexes:
        tgs = touch_points_search(vertex, obj)
        for tg in tgs:
            if vertex != tg:
                line = LineFunction(vertex, tg)
                if not intersection(vertex, tg, polygon) and not intersection(vertex, tg, obj):
                    f = line.a is not None
                    f = line not in tangents
                    if f:
                        tangents.append(line)
    return tangents


def tangent_points_polygons(tangent: LineFunction, polygon1: Polygon, polygon2: Polygon):
    """
        Находит точки пересечения линии касательной с двумя многоугольниками.

        Args:
            tangent (LineFunction): Линия касательная
            polygon1 (Polygon): Первый многоугольник
            polygon2 (Polygon): Второй многоугольник

        Returns:
            list: Список точек пересечения
            """
    points = [None, None]
    vertexes1 = polygon1.vertexes
    vertexes2 = polygon2.vertexes
    for vertex in vertexes1:
        if tangent.substitute(vertex) <= EPS:
            points[0] = vertex
    for vertex in vertexes2:
        if tangent.substitute(vertex) <= EPS:
            points[1] = vertex
    return points


def tangent_points_polygon_circle(tangent: LineFunction, polygon: Polygon, circle: Circle):
    """
        Находит точки пересечения линии касательной с кругом и многоугольником.

        Args:
            tangent (LineFunction): Линия касательная
            polygon (Polugon): многоугольник
            circle (Circle): Круг

        Returns:
            Tuple[Point2D, Point2D]: Две точки пересечения
    """
    points = [None, None]
    vertexes = polygon.vertexes
    for vertex in vertexes:
        if tangent.substitute(vertex) <= EPS:
            points[0] = vertex
    circ_tgs = circle_touch_points(points[0], circle)
    for tg in circ_tgs:
        if tangent.substitute(tg) <= EPS:
            points[1] = tg
    return points


def tangents_between(object1: Union[Circle, Polygon], object2: Union[Circle, Polygon]):
    """
        Нахождение линий касательных между двумя объектами.

        Args:
            object1 (Union[Circle, Polygon]): Объект для определения касания (круг или многоугольник)
            object2 (Union[Circle, Polygon]): Объект для определения касания (круг или многоугольник)

        Returns:
            List[LineFunction]: Список линий касательных
            """
    if isinstance(object1, Circle) and isinstance(object2, Circle):
        return tangents_between_circles(object1, object2)
    else:
        if isinstance(object1, Polygon):
            return tangents_between_polygon(object1, object2)
        else:
            return tangents_between_polygon(object2, object1)
