import math

def cuboid_volume(length, width, height):
    v = length * width * height
    return v


def cube_volume(length):
    v = length * length * length
    return v


def prism_volume(base, height):
    v = base * height
    return v


def cylinder_volume(radius, height):
    v = math.pi()*(radius*radius)*height
    return v

def sphere_volume(radius):
    v = (4/3)*math.pi*(radius * radius * radius)
    return v

def pyramid_volume(base, height):
    v = (1/3) * base * height
    return v

def sq_pyramid_volume(length, width, height):
    v = (1/3)* length * width * height
    return v

