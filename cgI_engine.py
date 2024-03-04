from vertex import Vertex


class CGIengine:
    def __init__(self, myWindow, defaction):
        self.w_width = myWindow.width
        self.w_height = myWindow.height
        self.win = myWindow
        self.keypressed = 1
        self.default_action = defaction

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

    def drawTriangles(self, vertex_pos, colors, indices):
        for i in range(0, len(indices), 3):
            triangle_indices = indices[i:i + 3]

            vertices = []
            for index in triangle_indices:
                x = vertex_pos[2 * index]
                y = vertex_pos[(2 * index) + 1]
                r = colors[(3 * index)]
                g = colors[(3 * index) + 1]
                b = colors[(3 * index) + 2]
                vertices.append(Vertex(x, y, r, g, b))
            self.rasterizeTriangle(vertices[0], vertices[1], vertices[2])

    def rasterizeTriangle(self, p0, p1, p2):
        min_x = min(p0.x, p1.x, p2.x)
        max_x = max(p0.x, p1.x, p2.x)
        min_y = min(p0.y, p1.y, p2.y)
        max_y = max(p0.y, p1.y, p2.y)

        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                edge_function01 = self.calculateEdgeFunction(p0, p1, x, y)
                edge_function12 = self.calculateEdgeFunction(p1, p2, x, y)
                edge_function20 = self.calculateEdgeFunction(p2, p0, x, y)

                if (edge_function01 >= 0 and edge_function12 >= 0 and edge_function20 >= 0) or (
                        edge_function01 <= 0 and edge_function12 <= 0 and edge_function20 <= 0):
                    total_area = abs(
                        0.5 * self.calculateEdgeFunction(p1, p2, p0.x, p0.y))

                    if total_area == 0.0:
                        total_area = 1

                    # Calculate barycentric coordinates.
                    alpha = edge_function12 / (2 * total_area)
                    beta = edge_function20 / (2 * total_area)
                    gamma = edge_function01 / (2 * total_area)

                    pixel_color = (
                        int(alpha * p0.r + beta * p1.r + gamma * p2.r),
                        int(alpha * p0.g + beta * p1.g + gamma * p2.g),
                        int(alpha * p0.b + beta * p1.b + gamma * p2.b)
                    )

                    self.win.set_pixel(x, y, pixel_color[0], pixel_color[1],
                                       pixel_color[2])

    def calculateEdgeFunction(self, p0, p1, x, y):
        return (x - p0.x) * (p1.y - p0.y) - (y - p0.y) * (p1.x - p0.x)

    # go is called on every update of the window display loop
    # have your engine draw stuff in the window.
    def go(self):
        if (self.keypressed == 1):
            # default scene
            self.default_action()


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