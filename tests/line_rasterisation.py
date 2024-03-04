from cgI_engine import *
from rit_window import *

def default_action():
    # draw your double row of houses here
    myEngine.win.clearFB(0, 0, 0)
    myEngine.rasterizeLine(100, 100, 500, 500, 255, 0, 0)  # red
    myEngine.rasterizeLine(100, 200, 500, 400, 0, 255, 0)  # green
    myEngine.rasterizeLine(100, 300, 500, 300, 0, 0, 255)  # blue
    myEngine.rasterizeLine(100, 400, 500, 200, 255, 255, 0)  # yellow
    myEngine.rasterizeLine(100, 500, 500, 100, 0, 255, 255)  # dark cyan
    myEngine.rasterizeLine(200, 500, 400, 100, 255, 0, 255)  # pink
    myEngine.rasterizeLine(300, 500, 300, 100, 255, 255, 255)  # white
    myEngine.rasterizeLine(400, 500, 200, 100, 128, 255, 255)  # cyan
    myEngine.rasterizeLine(500, 450, 100, 150, 34, 200, 10)  # parrot green
    myEngine.rasterizeLine(450, 100, 150, 500, 34, 200, 140)  # dark green

window = RitWindow(800, 800)
myEngine = CGIengine(window, default_action)

def main():
    window.run(myEngine)


if __name__ == "__main__":
    main()