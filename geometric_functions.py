from math import *
import classes

INF = 10 ** 8


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

    return [classes.Point2D(t1x, t1y), classes.Point2D(t2x, t2y)]


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
