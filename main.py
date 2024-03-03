from rit_window import *
from cgI_engine import *

def main():
    window = RitWindow(800, 800)
    myEngine = CGIengine (window)
    
    window.run (myEngine)

if __name__ == "__main__":
    main()
