"""

Methods that don't belong to any particular class, particularly of a generic, mathematical nature.

"""

import math


def cross(a, b):
    """The cross product between vectors a and b. This code was copied off of StackOverflow, but it's better than
    making you download numpy."""
    c = (a[1] * b[2] - a[2] * b[1],
         a[2] * b[0] - a[0] * b[2],
         a[0] * b[1] - a[1] * b[0])

    return c


def dot(a, b):
    """The dot product between vectors a and b."""
    c = sum(a[i] * b[i] for i in range(len(a)))

    return c


def bilinear_interp(array, point):
    """Interpolate between the values at the integer-positions around the given float-position in the given array."""
    x = point[0]
    y = point[1]

    x_lower = math.floor(x)
    x_upper = x_lower + 1
    y_lower = math.floor(y)
    y_upper = y_lower + 1

    return (array[x_lower, y_lower] * (x_upper - x) * (y_upper - y) +
            array[x_lower, y_upper] * (x_upper - x) * (y - y_lower) +
            array[x_upper, y_lower] * (x - x_lower) * (y_upper - y) +
            array[x_upper, y_upper] * (x - x_lower) * (y - y_lower)
            )