class CGIengine:
    def __init__(self, myWindow, defaction):
        # Initialize the CGIengine with a window and a default action
        self.w_width = myWindow.width  # Store the window's width
        self.w_height = myWindow.height  # Store the window's height
        self.win = myWindow  # Store the window object
        self.keypressed = 1  # Set an initial keypressed value to 1
        self.default_action = defaction  # Store the default action

    def rasterizeTriangle(self, p0, p1, p2):
        pass

    def drawTriangles(self, vertex_pos, colors, indices):
        pass

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

    def rasterizeLine(self, x0, y0, x1, y1, r, g, b):
        dy = y1 - y0
        dx = x1 - x0
        x, y = x0, y0

        # when slope is infinite
        if dx == 0:
            for y_value in range(y1, y0):
                self.win.set_pixel(x, y_value, r, g, b)

        # when slope is 0
        elif dy == 0:
            for x_value in range(x0, x1):
                self.win.set_pixel(x_value, y, r, g, b)

        # when slope is positive
        elif dy > 0 and dx > 0 or dy < 0 and dx < 0:
            # initialize x and y for plotting
            ystart, yend = min(y0, y1), max(y0, y1)
            xstart, xend = min(x0, x1), max(x0, x1)
            x, y = xstart, ystart

            # when slope between 0 and 1
            if 0 < dy / dx < 1:
                d = (2 * dy) - dx
                for x_value in range(xstart, xend):
                    self.win.set_pixel(x_value, y, r, g, b)
                    if d <= 0:
                        if y0 < y1 and x0 < x1:
                            d += (2 * dy)
                        else:
                            d -= (2 * dy)
                    else:
                        y += 1
                        if y0 < y1 and x0 < x1:
                            d += (2 * (dy - dx))
                        else:
                            d -= (2 * (dy - dx))
            # when slope greater than 1
            elif dy / dx >= 1:
                d = (2 * dx) - dy
                for y_cod in range(ystart, yend):
                    self.win.set_pixel(x, y_cod, r, g, b)
                    if d <= 0:
                        d -= (2 * dx)
                    else:
                        x += 1
                        d -= (2 * (dx - dy))
        # when slope is negative
        else:
            x, y = x0, y0
            # when slope between -1 and 0
            if 0 > dy / dx > -1:
                d = (2 * dy) + dx
                for x_value in range(x0, x1):
                    self.win.set_pixel(x_value, y, r, g, b)
                    if d <= 0:
                        y -= 1
                        d += (2 * (dy + dx))
                    else:
                        d += (2 * dy)
            # when slope less than -1
            elif dy / dx <= -1:
                d = (2 * dx) + dy
                ystart, yend = min(y0, y1), max(y0, y1)
                x = max(x0, x1)
                for y_value in range(ystart, yend):
                    self.win.set_pixel(x, y_value, r, g, b)
                    if d <= 0:
                        x -= 1
                        if y0 < y1:
                            d += (2 * (dy + dx))
                        else:
                            d -= (2 * (dy + dx))
                    else:
                        if y0 < y1:
                            d += (2 * dx)
                        else:
                            d -= (2 * dx)

    # go is called on every update of the window display loop
    # have your engine draw stuff in the window.
    def go(self):
        if (self.keypressed == 1):
            # default scene
            self.default_action()
            self.rasterizeLine(100, 100, 500, 500, 255, 0, 0)  # red
            self.rasterizeLine(100, 200, 500, 400, 0, 255, 0)  # green
            self.rasterizeLine(100, 300, 500, 300, 0, 0, 255)  # blue
            self.rasterizeLine(100, 400, 500, 200, 255, 255, 0)  # yellow
            self.rasterizeLine(100, 500, 500, 100, 0, 255, 255)  # dark cyan
            self.rasterizeLine(200, 500, 400, 100, 255, 0, 255)  # pink
            self.rasterizeLine(300, 500, 300, 100, 255, 255, 255)  # white
            self.rasterizeLine(400, 500, 200, 100, 128, 255, 255)  # cyan
            self.rasterizeLine(500, 450, 100, 150, 34, 200, 10)  # parrot green
            self.rasterizeLine(450, 100, 150, 500, 34, 200, 140)  # dark green

        if (self.keypressed == 2):
            # NK initials
            self.win.clearFB(0, 0, 0)
            self.rasterizeLine(150, 550, 150, 250, 255, 255, 255)
            self.rasterizeLine(350, 550, 350, 250, 255, 255, 255)
            self.rasterizeLine(150, 550, 350, 250, 255, 255, 255)
            self.rasterizeLine(450, 550, 450, 250, 255, 255, 255)
            self.rasterizeLine(450, 400, 700, 550, 255, 255, 255)
            self.rasterizeLine(450, 400, 700, 250, 255, 255, 255)



        # push the window's framebuffer to the window
        self.win.applyFB()

    def keyboard(self, key):
        if (key == '1'):
            self.keypressed = 1
            self.go()
        if (key == '2'):
            self.keypressed = 2
            self.go()