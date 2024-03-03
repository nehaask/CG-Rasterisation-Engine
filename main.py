from cgI_engine import *
from rit_window import *

def default_action():
    # draw your double row of houses here
    myEngine.win.clearFB(0, 0, 0)

window = RitWindow(800, 800)
myEngine = CGIengine(window, default_action)

def main():
    window.run(myEngine)


if __name__ == "__main__":
    main()