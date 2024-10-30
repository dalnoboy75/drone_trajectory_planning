from math import *
from geometry import classes

INF = 10 ** 8
EPS = 10 ** -6
ROUND_NUM = 6


# Расчёт количества точек пересечения с окружностью
def intersection_number(a: classes.Point2D, b: classes.Point2D, circle: classes.Circle):
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
        return 2
    elif d == 0:
        return 1
    else:
        return 0


# Поиск точек касания касательных от точки с окружностью
def touch_points_search(point: classes.Point2D, circle: classes.Circle):
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
