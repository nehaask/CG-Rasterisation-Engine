from cgI_engine import *
from rit_window import *
from vertex import *


def default_action():
    myEngine.win.clearFB(0, 0, 0)
    P0 = Vertex(100, 100, 255, 0, 0)
    P1 = Vertex(300, 300, 0, 255, 0)
    P2 = Vertex(400, 100, 0, 0, 255)
    myEngine.rasterizeTriangle(P0, P1, P2)

    P0 = Vertex(500, 200, 255, 0, 0)
    P2 = Vertex(600, 150, 128, 128, 0)
    P1 = Vertex(600, 400, 50, 0, 50)
    myEngine.rasterizeTriangle(P0, P1, P2)

    P0 = Vertex(100, 500, 0, 255, 0)
    P1 = Vertex(300, 700, 0, 200, 0)
    P2 = Vertex(400, 500, 0, 100, 0)
    myEngine.rasterizeTriangle(P0, P1, P2)


window = RitWindow(800, 800)
myEngine = CGIengine(window, default_action)


def main():
    window.run(myEngine)


if __name__ == "__main__":
    main()