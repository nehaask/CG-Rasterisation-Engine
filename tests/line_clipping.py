from rit_window import *
from cgI_engine import *
from vertex import *
from clipper import *
import numpy as np

line1 = np.array([25, 50, 20, 150]);
line2 = np.array([75, 100, 100, 75]);
line3 = np.array([25, 175, 100, 180]);
line4 = np.array([200, 175, 275, 100]);
line5 = np.array([175, 230, 275, 200]);
line6 = np.array([25, 280, 280, 10]);


def drawClippedLine(E, cL, r, g, b):
    P0 = Vertex(round(cL[0].x), round(cL[0].y), r, g, b)
    P1 = Vertex(round(cL[1].x), round(cL[1].y), r, g, b)
    E.rasterizeLine(P0.x, P0.y, P1.x, P1.y, r, g, b)


def default_action():
    # clear the FB
    myEngine.win.clearFB(0, 0, 0)

    # draw the clip window
    myEngine.win.drawRect(250, 50, 225, 50, 255, 255, 255)

    # first line: totally outside
    P0 = Vertex(line1[0], line1[1], 255, 255, 255)
    P1 = Vertex(line1[2], line1[3], 255, 255, 255)
    myEngine.rasterizeLine(P0.x, P0.y, P1.x, P1.y, 255, 255, 255)
    clippedLine = clipLine(P0, P1, 250, 50, 225, 50);
    if clippedLine.any():
        drawClippedLine(myEngine, clippedLine, 255, 0, 0)

    #  second line: totally inside
    P0 = Vertex(line2[0], line2[1], 255, 255, 255)
    P1 = Vertex(line2[2], line2[3], 255, 255, 255)
    myEngine.rasterizeLine(P0.x, P0.y, P1.x, P1.y, 255, 255, 255)
    clippedLine = clipLine(P0, P1, 250, 50, 225, 50);
    if clippedLine.any():
        drawClippedLine(myEngine, clippedLine, 0, 255, 0)

    #  third line: outside on left
    P0 = Vertex(line3[0], line3[1], 255, 255, 255)
    P1 = Vertex(line3[2], line3[3], 255, 255, 255)
    myEngine.rasterizeLine(P0.x, P0.y, P1.x, P1.y, 255, 255, 255)
    clippedLine = clipLine(P0, P1, 250, 50, 225, 50);
    if clippedLine.any():
        drawClippedLine(myEngine, clippedLine, 0, 0, 255)

    # fourth line: outside on right
    P0 = Vertex(line4[0], line4[1], 255, 255, 255)
    P1 = Vertex(line4[2], line4[3], 255, 255, 255)
    myEngine.rasterizeLine(P0.x, P0.y, P1.x, P1.y, 255, 255, 255)
    clippedLine = clipLine(P0, P1, 250, 50, 225, 50);
    if clippedLine.any():
        drawClippedLine(myEngine, clippedLine, 255, 0, 255)

    #  fifth line: outside on right and left
    P0 = Vertex(line5[0], line5[1], 255, 255, 255)
    P1 = Vertex(line5[2], line5[3], 255, 255, 255)
    myEngine.rasterizeLine(P0.x, P0.y, P1.x, P1.y, 255, 255, 255)
    clippedLine = clipLine(P0, P1, 250, 50, 225, 50);
    if clippedLine.any():
        drawClippedLine(myEngine, clippedLine, 0, 255, 255)

    #  sixth line: cut on all sides
    P0 = Vertex(line6[0], line6[1], 255, 255, 255)
    P1 = Vertex(line6[2], line6[3], 255, 255, 255)
    myEngine.rasterizeLine(P0.x, P0.y, P1.x, P1.y, 255, 255, 255)
    clippedLine = clipLine(P0, P1, 250, 50, 225, 50);
    if clippedLine.any():
        drawClippedLine(myEngine, clippedLine, 255, 255, 0)


window = RitWindow(400, 400)
myEngine = CGIengine(window, default_action)


def main():
    window.run(myEngine)


if __name__ == "__main__":
    main()
