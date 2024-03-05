from cgI_engine import *
from rit_window import *

house_data = np.array([0, 0, 0, 50, 50, 50, 50, 0, 0, 50, 25, 75, 50, 50])
house_index_data = np.array([0, 1, 2, 0, 2, 3, 4, 5, 6])
house_color_data = np.array([255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 0, 255, 0, 0, 255, 0, 0, 255,
     0])


def default_action():
    # clear the FB
    myEngine.win.clearFB(0, 0, 0)

    # draw the untransformed house
    myEngine.drawTriangles(house_data, house_color_data, house_index_data)

    # translate the house
    myEngine.translate(100.0, 500.0)
    myEngine.drawTriangles(house_data, house_color_data, house_index_data)

    # scale then translate
    myEngine.clearModelTransform()
    myEngine.scale(3.5, 4.1)
    myEngine.translate(300.0, 400.0)
    myEngine.drawTriangles(house_data, house_color_data, house_index_data)

    # rotate then translate
    myEngine.clearModelTransform()
    myEngine.rotate(60.0)
    myEngine.translate(600.0, 400.0)
    myEngine.drawTriangles(house_data, house_color_data, house_index_data)

    # zoom in on translated house and then stretch on bottom of screen
    myEngine.clearModelTransform()
    myEngine.translate(100.0, 500.0)
    myEngine.defineClipWindow(576, 499, 151, 100)
    myEngine.defineViewWindow(200, 50, 750, 150)
    myEngine.drawTriangles(house_data, house_color_data, house_index_data)


window = RitWindow(800, 800)
myEngine = CGIengine(window, default_action)


def main():
    window.run(myEngine)


if __name__ == "__main__":
    main()