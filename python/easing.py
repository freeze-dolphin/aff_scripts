import math


def ease_linear(x):
    return x


def ease_in_cubic(x):
    return x * x * x


def ease_in_out_cubic(x: float) -> float:
    if x < 0.5:
        return 4 * x * x * x
    else:
        return 1 - pow(-2 * x + 2, 3) / 2


def ease_in_out_sine(x: float) -> float:
    return -(math.cos(math.pi * x) - 1) / 2


def ease_out_cubic(x):
    return 1 - pow(1 - x, 3)


def ease_in_sine(x):
    return 1 - math.cos(x * math.pi / 2)


def ease_out_sine(x):
    return math.sin(x * math.pi / 2)


def ease_out_quad(x: float) -> float:
    return 1 - (1 - x) * (1 - x)


def ease_in_expo(x: float) -> float:
    return 0 if x == 0 else math.pow(2, 10 * x - 10)


def ease_in_out_back(x):
    c1 = 1.70158
    c2 = c1 * 1.525
    if x < 0.5:
        return (2 * x ** 2 * ((c2 + 1) * 2 * x - c2)) / 2
    else:
        return ((2 * x - 2) ** 2 * ((c2 + 1) * (2 * x - 2) + c2) + 2) / 2


def ease_out_bounce(x):
    n1 = 7.5625
    d1 = 2.75
    if x < 1 / d1:
        return n1 * x * x
    elif x < 2 / d1:
        x -= 1.5 / d1
        return n1 * x * x + 0.75
    elif x < 2.5 / d1:
        x -= 2.25 / d1
        return n1 * x * x + 0.9375
    else:
        x -= 2.625 / d1
        return n1 * x * x + 0.984375
