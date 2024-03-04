import numpy as np
from bitarray import bitarray

from vertex import Vertex

CENTRE = bitarray('0000')

def compute_outcode(x, y, top, bottom, right, left):
    outcode = bitarray()
    outcode.extend([
        int(y > top),  # Bit 0: Above
        int(y < bottom),  # Bit 1: Below
        int(x > right),  # Bit 2: Right
        int(x < left)  # Bit 3: Left
    ])
    return outcode

def clipLine(P0, P1, top, bottom, right, left):
    point1 = compute_outcode(P0.x, P0.y, top, bottom, right, left)
    point2 = compute_outcode(P1.x, P1.y, top, bottom, right, left)
    slope = (P1.y - P0.y) / (P1.x - P0.x)
    intercept = P1.y - slope * P1.x

    while True:
        # trivial accept
        if (point1 | point2) == CENTRE:
            return np.asarray([P0, P1])
        # trivial reject
        if (point1 & point2) != CENTRE:
            return np.array([])
        # point1 is outside
        if point1 != CENTRE:
            if point1[2] == 1:
                P0.x, P0.y = right, (slope * right) + intercept
            elif point1[3] == 1:
                P0.x, P0.y = left, (slope * left) + intercept
            elif point1[0] == 1:
                P0.x, P0.y = (top - intercept) / slope, top
            elif point1[1] == 1:
                P0.x, P0.y = (bottom - intercept) / slope, bottom
        # point2 is outside
        if point2 != CENTRE:
            if point2[2] == 1:
                P1.x, P1.y = right, (slope * right) + intercept
            elif point2[3] == 1:
                P1.x, P1.y = left, (slope * left) + intercept
            elif point2[0] == 1:
                P1.x, P1.y = (top - intercept) / slope, top
            elif point2[1] == 1:
                P1.x, P1.y = (bottom - intercept) / slope, bottom
        return np.asarray([P0, P1])

def clipPoly(vertices, top, bottom, right, left):
    def is_inside(p, edge):
        if edge == "top":
            return p.y <= top
        elif edge == "bottom":
            return p.y >= bottom
        elif edge == "left":
            return p.x >= left
        elif edge == "right":
            return p.x <= right

    def intersection(p1, p2, edge):
        if edge == "top":
            t = (top - p1.y) / (p2.y - p1.y)
        elif edge == "bottom":
            t = (bottom - p1.y) / (p2.y - p1.y)
        elif edge == "left":
            t = (left - p1.x) / (p2.x - p1.x)
        elif edge == "right":
            t = (right - p1.x) / (p2.x - p1.x)

        ix = p1.x + t * (p2.x - p1.x)
        iy = p1.y + t * (p2.y - p1.y)

        return Vertex(ix, iy, p1.r, p1.g, p1.b)

    def clip_polygon_edge(subject, edge):
        if len(subject) == 0:
            return np.array([])
        else:
            output = []
            s = subject[-1]

            for p in subject:
                if is_inside(p, edge):
                    if not is_inside(s, edge):
                        output.append(intersection(s, p, edge))
                    output.append(p)
                elif is_inside(s, edge):
                    output.append(intersection(p, s, edge))
                s = p
            return output

    result = vertices
    for edge in ["right", "top", "bottom", "left"]:
        result = clip_polygon_edge(result, edge)
    return np.asarray(result)
