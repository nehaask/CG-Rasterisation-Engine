from cgI_engine import CGIengine
from rit_window import *

vertex_data = np.array([100, 100, 300, 300, 400, 100, 500, 200, 600, 150, 600, 400, 100, 500, 300,700, 400, 500])
index_data = np.array([0, 1, 2, 3, 5, 4, 6, 7, 8])
color_data = np.array([255, 0, 0, 0, 255, 0, 0, 0, 255, 255, 0, 0, 128, 128, 0, 50, 0, 50, 0, 255, 0, 0, 200, 0, 0, 100, 0])


def default_action():
    myEngine.win.clearFB(0, 0, 0)
    myEngine.drawTriangles(vertex_data, color_data, index_data)


window = RitWindow(800, 800)
myEngine = CGIengine(window, default_action)


def main():
    window.run(myEngine)


if __name__ == "__main__":
    main()