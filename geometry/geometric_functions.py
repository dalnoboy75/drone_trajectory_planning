from math import *
from typing import Union

from geometry import classes
from geometry.classes import Point2D

INF = 10 ** 8
EPS = 10 ** -6
ROUND_NUM = 6


# Расчёт количества точек пересечения с окружностью
def circle_intersection(a: classes.Point2D, b: classes.Point2D, circle: classes.Circle):
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

def polygon_intersection(a:classes.Point2D, b:classes.Point2D, polygon: classes.Polygon):
    line = classes.LineFunction(a,b)
    vertexes = polygon.vertexes
    for i in range(len(vertexes)):
        v = classes.LineFunction(vertexes[i],vertexes[(i+1)%len(vertexes)])
        if line.substitute(vertexes[i]) * line.substitute(vertexes[(i+1)% len(vertexes)]) < -EPS and v.substitute(a)*v.substitute(b) < -EPS:
            return True

    pr = INF
    for i in range(len(vertexes)):
        if abs(line.substitute(vertexes[i])) <= EPS:
            if (pr + 1) % INF == 0 or i - pr == 1 or i - pr == len(vertexes) - 1:
                pr = i
            else:
                return True
    return False

# Поиск точек касания касательных от точки с окружностью
def touch_points_search(point: classes.Point2D, object: Union[classes.Circle, classes.Polygon]):
    if isinstance(object, classes.Circle):
        return circle_touch_points(point, object)
    elif isinstance(object, classes.Polygon):
        return polygon_touch_points(point, object)


def circle_touch_points(point:classes.Point2D, circle: classes.Circle):
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
def polygon_touch_points(point:classes.Point2D, polygon:classes.Polygon):
    center = Point2D(0,0)
    vertexes = polygon.vertexes
    for ver in vertexes:
        center.x += ver.x
        center.y += ver.y
    center.x /= len(vertexes)
    center.y /= len(vertexes)

    tp1 = vertexes[0]
    tp2 = Point2D()
    cos_alpha_1 = cos_alpha_2= 1.0
    center_dist = calc_dist(center, point)
    line = classes.LineFunction(center, point)

    for vertex in vertexes:
        if (line.substitute(vertex) * line.substitute(tp1)) < 0:
            tp2 = vertex
            break

    for vertex in vertexes:
        vertex_dist = calc_dist(vertex, point)
        center_vertex_dist= calc_dist(center,vertex)
        new_cos_alpha = (vertex_dist**2 + center_dist**2 - center_vertex_dist**2)/(2*vertex_dist*center_dist)
        if line.substitute(vertex)* line.substitute(tp1) > 0 and new_cos_alpha < cos_alpha_1:
            cos_alpha_1 = new_cos_alpha
            tp1 = vertex
        if line.substitute(vertex)* line.substitute(tp2) > 0 and new_cos_alpha < cos_alpha_2:
            cos_alpha_2 = new_cos_alpha
            tp2 = vertex

    return tp1,tp2


# Расчёт расстояния между двумя точками
def calc_dist(first_point: classes.Point2D, second_point: classes.Point2D):
    return hypot(first_point.x - second_point.x, first_point.y - second_point.y)


# Расчёт длины дуги между двумя точками на окружности
def arc_length(first_point: classes.Point2D, second_point: classes.Point2D, circle: classes.Circle):
    chord = calc_dist(first_point, second_point)
    try:
        angle = acos((2 * circle.radius ** 2 - chord ** 2) / (2 * circle.radius ** 2))
    except:
        return INF
    return angle * circle.radius


def tangents_between_circles(circle1: classes.Circle, circle2: classes.Circle):
    tangents = []
    x0 = circle1.center.x
    y0 = circle1.center.y
    x1 = circle2.center.x
    y1 = circle2.center.y
    r0 = circle1.radius
    r1 = circle2.radius

    def find_tangent(r_0, r_1):
        a = b = c = None
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
        return [a, b, c]

    for n1 in [-1, 1]:
        for n2 in [-1, 1]:
            t = find_tangent(r0 * n1, r1 * n2)
            is_unique = t[0] is not None
            if t in tangents:
                is_unique = False
            if is_unique:
                tangents.append(t)
    return tangents


def tangent_points(tangent: list, circle1: classes.Circle, circle2: classes.Circle):
    a, b, c = tangent
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

def dist_between__poly_points(a:classes.Point2D, b: classes.Point2D, polygon:classes.Polygon):
    pass