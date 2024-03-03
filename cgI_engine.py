class CGIengine:
    def __init__(self, myWindow):
        self.w_width = myWindow.width
        self.w_height = myWindow.height
        self.win = myWindow
        self.keypressed = 1

    def draw_star(self, pixel_x, pixel_y, r, g, b):
        for x in range(pixel_x - 7, pixel_x + 8):
            for y in range(pixel_y - 7, pixel_y + 8):
                self.win.set_pixel(x, y, r, g, b)

        for x in range(pixel_x - 15, pixel_x + 16):
            for y in range(pixel_y - 2, pixel_y + 2):
                self.win.set_pixel(x, y, r, g, b)

        for y in range(pixel_y - 15, pixel_y + 16):
            for x in range(pixel_x - 2, pixel_x + 2):
                self.win.set_pixel(x, y, r, g, b)

    # go is called on every update of the window display loop
    # have your engine draw stuff in the window.
    def go(self):
        if (self.keypressed == 1):

            # default scene
            self.win.clearFB(0, 50, 100)
            for x in range(20, 50):
                for y in range(self.w_height):
                    self.win.set_pixel(x, y, 255, 0, 0)

        if (self.keypressed == 2):

            self.win.clearFB(0, 0, 0)
            for x in range(self.w_width // 5, self.w_width - 1,
                           self.w_width // 5):
                for y in range(self.w_width // 5, self.w_height - 1,
                               self.w_height // 5):
                    if (y / 160) % 2 != 0:
                        if (x / 160) % 2 != 0:
                            self.draw_star(x, y, 128, 255, 255)
                        else:
                            self.draw_star(x, y, 34, 200, 10)
                    else:
                        if (x / 160) % 2 != 0:
                            self.draw_star(x, y, 255, 0, 0)
                        else:
                            self.draw_star(x, y, 0, 255, 255)

        # push the window's framebuffer to the window
        self.win.applyFB()

    def keyboard(self, key):
        if (key == '1'):
            self.keypressed = 1
            self.go()
        if (key == '2'):
            self.keypressed = 2
            self.go()