import math


def rect_prism(length, width, height):
    sa = 2 * (length * width) + (2 * (length * height)) + (2 * (width * height))
    return sa


def irregular_prism(height, perimeter, base):
    sa = height * perimeter + 2 * base
    return sa


def cylinder(radius, height):
    sa = 2 * math.pi * (radius * radius) + 2 * math.pi * radius * height
    return round(sa, 1)


def trapizoid(perimeter, base1, base2, height1, height_of_base):
    # Finding the surface area of a trapezoid with 2 different bases
    b = height1 / 2 * (base1 + base2)
    sa = height_of_base * perimeter + 2 * b
    return sa


def cones(radius, slant_height):
    sa = math.pi * (radius * radius) + math.pi * radius * slant_height
    return round(sa, 1)


def pyramids(slant_height, base_perimeter, base_area):
    sa = (slant_height * base_perimeter) / 2 + base_area
    return sa
