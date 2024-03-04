from cgI_engine import *
from clipper import *
from rit_window import *
from vertex import *

vertex_data = np.array(
    [100, 100, 300, 300, 400, 100, 500, 200, 600, 150, 600, 400, 100, 500, 300,
     700, 400, 500])
index_data = np.array([0, 1, 2, 3, 5, 4, 6, 7, 8])
color_data = np.array(
    [255, 0, 0, 0, 255, 0, 0, 0, 255, 255, 0, 0, 128, 128, 0, 50, 0, 50, 0, 255,
     0, 0, 200, 0, 0, 100, 0])


# A simple routine to do a fan triangulation of a convex polygon
# and then rasterize each of the triangle
def drawClippedPoly(vertices):
    nverts = vertices.size
    if nverts < 3:
        return

    # chose your pivot vertex to be the first
    P0 = Vertex(round(vertices[0].x), round(vertices[0].y), vertices[0].r,
                vertices[0].g, vertices[0].b)
    endV = 2;
    while endV < nverts:
        P1 = Vertex(round(vertices[endV - 1].x), round(vertices[endV - 1].y),
                    vertices[endV - 1].r, vertices[endV - 1].g,
                    vertices[endV - 1].b)
        P2 = Vertex(round(vertices[endV].x), round(vertices[endV].y),
                    vertices[endV].r, vertices[endV].g, vertices[endV].b)
        myEngine.rasterizeTriangle(P0, P1, P2)
        endV = endV + 1


def default_action():
    myEngine.win.clearFB(0, 0, 0)

    # all in -- no clipping
    myEngine.win.drawRect(775, 625, 175, 25, 255, 255, 255)
    P0 = Vertex(50, 650, 255, 0, 0)
    P1 = Vertex(100, 750, 255, 0, 0)
    P2 = Vertex(150, 650, 255, 0, 0)
    Poly = np.array([P0, P1, P2])
    cP = clipPoly(Poly, 775, 625, 175, 25)
    if cP.any():
        drawClippedPoly(cP)

    # one out -- top - green
    myEngine.win.drawRect(775, 625, 350, 225, 255, 255, 255)
    P0 = Vertex(250, 650, 0, 255, 0)
    P1 = Vertex(300, 800, 0, 255, 0)
    P2 = Vertex(325, 650, 0, 255, 0)
    Poly = np.array([P0, P1, P2])
    cP = clipPoly(Poly, 775, 625, 350, 225)
    if cP.any():
        drawClippedPoly(cP)

    # one out -- bottom -- blue
    myEngine.win.drawRect(775, 625, 550, 425, 255, 255, 255)
    P0 = Vertex(450, 700, 0, 0, 255)
    P1 = Vertex(500, 130, 0, 0, 255)
    P2 = Vertex(525, 700, 0, 0, 255)
    Poly = np.array([P0, P2, P1])
    cP = clipPoly(Poly, 775, 625, 550, 425)
    if cP.any():
        drawClippedPoly(cP)

    # one out -- right -- cyan
    myEngine.win.drawRect(775, 625, 750, 625, 255, 255, 255)
    P0 = Vertex(650, 650, 0, 255, 255)
    P1 = Vertex(650, 725, 0, 255, 255)
    P2 = Vertex(900, 700, 0, 255, 255)
    Poly = np.array([P0, P1, P2])
    cP = clipPoly(Poly, 775, 625, 750, 625)
    if cP.any():
        drawClippedPoly(cP)

    # one out -- left -- magenta
    myEngine.win.drawRect(575, 425, 150, 25, 255, 255, 255)
    P0 = Vertex(100, 550, 255, 0, 255)
    P1 = Vertex(100, 450, 255, 0, 255)
    P2 = Vertex(10, 500, 255, 0, 255)
    Poly = np.array([P0, P1, P2])
    cP = clipPoly(Poly, 575, 425, 150, 25)
    if cP.any():
        drawClippedPoly(cP)

    # two out -- right/right -- yello
    myEngine.win.drawRect(575, 425, 350, 225, 255, 255, 255)
    P0 = Vertex(450, 550, 255, 255, 0)
    P1 = Vertex(550, 450, 255, 255, 0)
    P2 = Vertex(300, 500, 255, 255, 0)
    Poly = np.array([P0, P1, P2])
    cP = clipPoly(Poly, 575, 425, 350, 225)
    if cP.any():
        drawClippedPoly(cP)

    # two out -- right/left-- light red
    myEngine.win.drawRect(575, 425, 550, 425, 255, 255, 255)
    P0 = Vertex(400, 550, 128, 0, 0)
    P1 = Vertex(600, 550, 128, 0, 0)
    P2 = Vertex(500, 500, 128, 0, 0)
    Poly = np.array([P0, P1, P2])
    cP = clipPoly(Poly, 575, 425, 550, 425)
    if cP.any():
        drawClippedPoly(cP)

    # two out -- right/top-- light green
    myEngine.win.drawRect(575, 425, 750, 625, 455, 255, 255)
    P0 = Vertex(800, 550, 0, 128, 0)
    P1 = Vertex(675, 650, 0, 128, 0)
    P2 = Vertex(650, 590, 0, 128, 0)
    Poly = np.array([P0, P2, P1])
    cP = clipPoly(Poly, 575, 425, 750, 625)
    if cP.any():
        drawClippedPoly(cP)

    # two out -- right/bottom-- light blue
    myEngine.win.drawRect(375, 225, 175, 25, 455, 255, 255)
    P0 = Vertex(220, 350, 0, 0, 128)
    P1 = Vertex(150, 200, 0, 0, 128)
    P2 = Vertex(150, 300, 0, 0, 128)
    Poly = np.array([P0, P1, P2])
    cP = clipPoly(Poly, 375, 225, 175, 25)
    if cP.any():
        drawClippedPoly(cP)

    # two out -- left / left -- light cyan
    myEngine.win.drawRect(375, 225, 375, 225, 455, 255, 255)
    P0 = Vertex(200, 300, 0, 128, 128)
    P1 = Vertex(190, 250, 0, 128, 128)
    P2 = Vertex(300, 300, 0, 128, 128)
    Poly = np.array([P0, P2, P1])
    cP = clipPoly(Poly, 375, 225, 375, 225)
    if cP.any():
        drawClippedPoly(cP)

    # two out -- left / top -- light magenta
    myEngine.win.drawRect(375, 225, 575, 425, 455, 255, 255)
    P0 = Vertex(400, 300, 128, 0, 128)
    P1 = Vertex(450, 450, 128, 0, 128)
    P2 = Vertex(500, 300, 128, 0, 128)
    Poly = np.array([P0, P1, P2])
    cP = clipPoly(Poly, 375, 225, 575, 425)
    if cP.any():
        drawClippedPoly(cP)

    # two out -- left / bottom -- light yellow
    myEngine.win.drawRect(375, 225, 775, 625, 455, 255, 255)
    P0 = Vertex(600, 300, 128, 128, 0)
    P1 = Vertex(550, 100, 128, 128, 0)
    P2 = Vertex(700, 300, 128, 128, 0)
    Poly = np.array([P0, P2, P1])
    cP = clipPoly(Poly, 375, 225, 775, 625)
    if cP.any():
        drawClippedPoly(cP)

    # two out -- top / bottom -- lighter red
    myEngine.win.drawRect(175, 25, 175, 25, 455, 255, 255)
    P0 = Vertex(50, 200, 64, 0, 0)
    P1 = Vertex(150, 210, 64, 0, 0)
    P2 = Vertex(70, 100, 64, 0, 0)
    Poly = np.array([P0, P1, P2])
    cP = clipPoly(Poly, 175, 25, 175, 25)
    if cP.any():
        drawClippedPoly(cP)

    # three out -- left / top / bottom -- lighter green
    myEngine.win.drawRect(175, 25, 375, 225, 455, 255, 255)
    P0 = Vertex(175, 150, 0, 64, 0)
    P1 = Vertex(250, 210, 0, 64, 0)
    P2 = Vertex(270, 10, 0, 64, 0)
    Poly = np.array([P0, P1, P2])
    cP = clipPoly(Poly, 175, 25, 375, 225)
    if cP.any():
        drawClippedPoly(cP)

    # all out -- left / top / bottom -- lighter blue
    myEngine.win.drawRect(175, 25, 575, 425, 455, 255, 255)
    P0 = Vertex(425, 200, 0, 0, 64)
    P1 = Vertex(575, 200, 0, 0, 64)
    P2 = Vertex(450, 300, 0, 0, 64)
    Poly = np.array([P0, P2, P1])
    cP = clipPoly(Poly, 175, 25, 575, 425)
    if cP.any():
        drawClippedPoly(cP)

    # all consuming  -- light grey
    myEngine.win.drawRect(175, 25, 775, 625, 255, 255, 255)
    P0 = Vertex(600, 0, 128, 128, 128)
    P1 = Vertex(700, 800, 128, 128, 128)
    P2 = Vertex(800, 0, 128, 128, 128)
    Poly = np.array([P0, P1, P2])
    cP = clipPoly(Poly, 175, 25, 775, 625)
    if cP.any():
        drawClippedPoly(cP)


window = RitWindow(800, 800)
myEngine = CGIengine(window, default_action)


def main():
    window.run(myEngine)


if __name__ == "__main__":
    main()