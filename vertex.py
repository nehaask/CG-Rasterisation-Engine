class Vertex:
    def __init__(self, x, y, r, g, b):
        self.x = x
        self.y = y
        self.r = r
        self.g = g
        self.b = b

    def getTriangleMin(p0, p1, p2):
        V = Vertex(p0.x, p0.y, 0, 0, 0)
        if (p1.x < V.x):
            V.x = p1.x
        if (p2.x < V.x):
            V.x = p2.x
        if (p1.y < V.y):
            V.y = p1.y
        if (p2.y < V.y):
            V.y = p2.y

        return V

    def getTriangleMax(p0, p1, p2):
        V = Vertex(p0.x, p0.y, 0, 0, 0)
        if (p1.x > V.x):
            V.x = p1.x
        if (p2.x > V.x):
            V.x = p2.x
        if (p1.y > V.y):
            V.y = p1.y
        if (p2.y > V.y):
            V.y = p2.y

        return V
