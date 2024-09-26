from math import *

INF = 10**8

# Расчёт количества точек пересечения с окружностью
def intersection_number(a, b, circle):
    ax = a[0]
    ay = a[1]
    bx = b[0]
    by = b[1]
    ox = circle[0]
    oy = circle[1]
    r = circle[2]

    # Считаем коэф-ты кв. уравнения
    A = (bx - ax) ** 2 + (by - ay) ** 2
    B = (ax - ox) * (bx - ax) + (ay - oy) * (by - ay)
    C = (ax - ox) ** 2 + (ay - oy) ** 2 - r ** 2

    D = B ** 2 - A * C

    if D > 0:
        return 2
    elif D == 0:
        return 1
    else:
        return 0

#Поиск точек касания касательных от точки с окружностью
def touch_points_search(point, circle):
    lx = circle[0] - point[0]
    ly = circle[1] - point[1]
    l = sqrt(lx ** 2 + ly ** 2)
    r = circle[2]
    d = atan2(ly, lx)
    t = asin(r / l)
    t1x = r * sin(d - t) + circle[0]
    t1y = r * (-cos(d - t)) + circle[1]
    t2x = r * (-sin(d + t)) + circle[0]
    t2y = r * cos(d + t) + circle[1]

    return [(t1x, t1y), (t2x, t2y)]

#Расчёт расстояния между двумя точками
def calc_dist(first_point, second_point):
    return sqrt((first_point[0] - second_point[0])**2 + (first_point[1]-second_point[1])**2)

#Расчёт длины дуги между двумя точками на окружности
def arc_length(first_point,second_point, circle):
    center = [circle[0], circle[1]]
    a = calc_dist(first_point, second_point)
    b = calc_dist(first_point, center)
    c = calc_dist(second_point, center)
    try:
        angle = acos((b**2 + c**2 - a**2) / (2*b*c))
    except:
        return INF
    return angle * circle[2]
