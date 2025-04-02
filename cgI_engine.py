import copy

import glm
import numpy as np

from vertex import *


class CGIengine:
    def __init__(self, myWindow, defaction):
        self.w_width = myWindow.width
        self.w_height = myWindow.height
        self.win = myWindow
        self.keypressed = 1
        self.default_action = defaction
        self.model_matrix = glm.mat4(1.0)
        self.normalization_matrix = glm.mat4(1.0)
        self.view_matrix = glm.mat4(1.0)
        self.transformation_matrix = glm.mat4(1.0)  # transformation matrix
        self.transformation_stack = [
            glm.mat4(1.0)]  # stack to traverse through hierarchy
        self.viewing_transform = glm.mat4(1.0)  # viewing transform Assignment 7
        self.projection_transform = glm.mat4(
            1.0)  # projection matrix Assignment 7
        self.z_buffer = [[float('inf') for _ in range(self.w_width)] for _ in
                         range(self.w_height)]

        self.view_port = glm.mat4()
        self.view_port = glm.translate(self.view_port, glm.vec3(400, 400, 400))
        self.view_port = glm.scale(self.view_port, glm.vec3(400, 400, 400))

        self.ambient_color = glm.vec3(0.0, 0.0, 0.0)
        self.diffuse_color = glm.vec3(0.0, 0.0, 0.0)
        self.specular_color = glm.vec3(0.0, 0.0, 0.0)
        self.light_position = glm.vec3(0.0, 0.0, 0.0)
        self.light_color = glm.vec3(0.0, 0.0, 0.0)
        self.eye = glm.vec3(0.0, 0.0, 0.0)

    # Assignment 2 - Rasterize Line
    def rasterizeLine(self, x0, y0, x1, y1, r, g, b):
        dy = y1 - y0
        dx = x1 - x0
        # when slope is 0
        if dy == 0:
            x, y = x0, y0
            for x_cod in range(x0, x1):
                self.win.set_pixel(x_cod, y, r, g, b)
        # when slope is infinite
        elif dx == 0:
            x, y = x0, y0
            for y_cod in range(y1, y0):
                self.win.set_pixel(x, y_cod, r, g, b)
        # when slope is positive
        elif dy > 0 and dx > 0 or dy < 0 and dx < 0:
            # change start and end points for x and y-axis
            if y0 > y1:
                ystart, yend = y1, y0
            else:
                ystart, yend = y0, y1

            if x0 > x1:
                xstart, xend = x1, x0
            else:
                xstart, xend = x0, x1
            # initialize x and y for plotting
            x, y = xstart, ystart
            # if slope is between 0 and 1
            if 0 < dy / dx <= 1:
                d = (2 * dy) - dx
                for x_cod in range(xstart, xend):
                    self.win.set_pixel(x_cod, y, r, g, b)
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
            # if slope is greater than 1
            elif dy / dx > 1:
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
            # if slope is between -1 and 0
            if 0 > dy / dx >= -1:
                d = (2 * dy) + dx
                for x_cod in range(x0, x1):
                    self.win.set_pixel(x_cod, y, r, g, b)
                    if d <= 0:
                        y -= 1
                        d += (2 * (dy + dx))
                    else:
                        d += (2 * dy)
            else:
                d = (2 * dx) + dy
                if y1 > y0:
                    ystart, yend = y0, y1
                else:
                    ystart, yend = y1, y0
                if x1 > x0:
                    x = x1
                else:
                    x = x0
                for y_cod in range(ystart, yend):
                    self.win.set_pixel(x, y_cod, r, g, b)
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

    # Assignment 3 - Triangle
    def drawTriangles(self, vertex_data, color_data, index_data):
        for ind in range(0, len(index_data), 3):
            vertices = []
            for i in index_data[ind: ind + 3]:
                x, y = vertex_data[2 * i], vertex_data[2 * i + 1]
                r, g, b = color_data[3 * i], color_data[3 * i + 1], color_data[
                    3 * i + 2]
                vertices.append(Vertex(x, y, r, g, b))

            for i in range(len(vertices)):
                original_vertex = glm.vec3(vertices[i].x, vertices[i].y, 1)
                transformed_vertex = self.view_matrix * self.normalization_matrix * \
                                     self.model_matrix * original_vertex
                vertices[i].x = int(transformed_vertex.x)
                vertices[i].y = int(transformed_vertex.y)

            self.rasterizeTriangle(vertices[0], vertices[1], vertices[2])

    def rasterizeTriangle(self, p0, p1, p2, image):
        min_x = min(p0.x, p1.x, p2.x)
        max_x = max(p0.x, p1.x, p2.x)
        min_y = min(p0.y, p1.y, p2.y)
        max_y = max(p0.y, p1.y, p2.y)

        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                edge_function01 = self.calculateEdgeFunction(p0, p1, x, y)
                edge_function12 = self.calculateEdgeFunction(p1, p2, x, y)
                edge_function20 = self.calculateEdgeFunction(p2, p0, x, y)

                if edge_function01 >= 0 and edge_function12 >= 0 and edge_function20 >= 0:
                    total_area = abs(
                        0.5 * self.calculateEdgeFunction(p1, p2, p0.x,
                                                         p0.y))
                    if total_area == 0.0:
                        total_area = 1
                    # Calculate barycentric coordinates.
                    alpha = edge_function12 / (2 * total_area)
                    beta = edge_function20 / (2 * total_area)
                    gamma = edge_function01 / (2 * total_area)

                    # Calculate interpolated depth
                    interpolated_depth = alpha * p0.z + beta * p1.z + gamma * p2.z

                    # Calculate interpolated texture coordinates
                    tex_u = alpha * p0.u + beta * p1.u + gamma * p2.u
                    tex_v = alpha * p0.v + beta * p1.v + gamma * p2.v

                    if image == None:
                        tex_color = self.texture_procedural(tex_u, tex_v, 0.05,
                                                            0.1)
                    else:
                        tex_color = self.texture_image(tex_u, tex_v, image)

                    # Depth test
                    if interpolated_depth < self.z_buffer[x][y]:
                        self.z_buffer[x][y] = interpolated_depth

                        # Normalize color values
                        pixel_color = (
                            alpha * p0.r + beta * p1.r + gamma * p2.r,
                            alpha * p0.g + beta * p1.g + gamma * p2.g,
                            alpha * p0.b + beta * p1.b + gamma * p2.b
                        )

                        # Multiply by the sampled texture color
                        pixel_color = (
                            pixel_color[0] * tex_color[0],
                            pixel_color[1] * tex_color[1],
                            pixel_color[2] * tex_color[2]
                        )

                        self.win.set_pixel(x, y, pixel_color[0], pixel_color[1],
                                           pixel_color[2])

    # def texture_procedural(self, u, v):
    #     # Calculate procedural texture (example: checkerboard pattern)
    #     scale = 10
    #     value = np.sin(u * scale) * np.sin(v * scale)
    #     normalized_value = (value + 1) / 2  # Normalize to [0, 1]
    #
    #     # Assuming image is a 3-channel (RGB) image
    #     return int(normalized_value * 255), 23, 23  # Red color for procedural texture

    def texture_procedural(self, u, v, width, height):
        # Calculate procedural red brick texture based on both u and v

        u_repeat = int(u / width)
        if u_repeat % 2 == 0:
            color = (0.8, 0.4, 0.2)  # Brick color for even u repeats (brownish)
        else:
            color = (0.7, 0.1, 0.1)  # Brick color for odd u repeats (reddish)
        color = tuple(c - v * 0.2 for c in color)
        return tuple(int(max(0, min(c, 1)) * 255) for c in color)

    def texture_image(self, u, v, image):
        # Replace with the actual path to your texture image
        width, height = image.size

        # Ensure u and v are within the valid range [0, 1]
        u = max(0, min(u, 1))
        v = max(0, min(v, 1))

        # Convert texture coordinates to pixel coordinates
        x = int(u * (width - 1))
        y = int(v * (height - 1))

        # Sample the texture using the pixel coordinates
        r, g, b = image.getpixel((x, y))
        return r, g, b

    def calculateEdgeFunction(self, p0, p1, x, y):
        return (x - p0.x) * (p1.y - p0.y) - (y - p0.y) * (p1.x - p0.x)

    # Assignment 5 - The Transformer
    # set model transform matrix to identity

    # Assignment 6 - The 3D Object (Changed 2D to 3D)
    def clearModelTransform(self):
        self.model_matrix = glm.mat4(1.0)
        self.transformation_stack[-1] = glm.mat4(1.0)

    # multiply translate matrix to current model transform
    def translate(self, x, y, z):
        # translate along x, y and z axes
        # self.model_matrix[3][0] += x
        # self.model_matrix[3][1] += y
        # self.model_matrix[3][2] += z
        # self.transformation_stack[-1] = self.model_matrix * self.transformation_stack[-1]
        self.transformation_stack[-1] = glm.translate(
            self.transformation_stack[-1], glm.vec3(x, y, z))

    # multiply scale matrix to current model transform
    def scale(self, x, y, z):
        # scale_mat = glm.mat4(1.0)
        # scaling_matrix = glm.scale(scale_mat, glm.vec3(x, y, z))
        # self.model_matrix = self.model_matrix * scaling_matrix
        # self.transformation_stack[-1] = scaling_matrix * self.transformation_stack[-1]
        self.transformation_stack[-1] = glm.scale(self.transformation_stack[-1],
                                                  glm.vec3(x, y, z))

    # rotate object along x-axis
    def rotatex(self, angle):
        rotation_matrix = glm.mat4(1.0)
        rotation_matrix[1][1] = np.cos(np.deg2rad(angle))
        rotation_matrix[1][2] = np.sin(np.deg2rad(angle))
        rotation_matrix[2][1] = -np.sin(np.deg2rad(angle))
        rotation_matrix[2][2] = np.cos(np.deg2rad(angle))
        # self.model_matrix = self.model_matrix * rotation_matrix
        self.transformation_stack[-1] = self.transformation_stack[
                                            -1] * rotation_matrix

    # rotate object along y-axis
    def rotatey(self, angle):
        rotation_matrix = glm.mat4(1.0)
        rotation_matrix[0][0] = np.cos(np.deg2rad(angle))
        rotation_matrix[0][2] = -np.sin(np.deg2rad(angle))
        rotation_matrix[2][0] = np.sin(np.deg2rad(angle))
        rotation_matrix[2][2] = np.cos(np.deg2rad(angle))
        # self.model_matrix = self.model_matrix * rotation_matrix
        self.transformation_stack[-1] = self.transformation_stack[
                                            -1] * rotation_matrix

    # rotate object along z-axis
    def rotatez(self, angle):
        rotation_matrix = glm.mat4(1.0)
        rotation_matrix[0][0] = np.cos(np.deg2rad(angle))
        rotation_matrix[0][1] = np.sin(np.deg2rad(angle))
        rotation_matrix[1][0] = -np.sin(np.deg2rad(angle))
        rotation_matrix[1][1] = np.cos(np.deg2rad(angle))
        # self.model_matrix = self.model_matrix * rotation_matrix
        self.transformation_stack[-1] = self.transformation_stack[
                                            -1] * rotation_matrix

    # get the normalization window
    def defineClipWindow(self, t, b, r, l):
        self.normalization_matrix[0][0] = (2 / (r - l))
        self.normalization_matrix[1][1] = (2 / (t - b))
        self.normalization_matrix[2][0] = ((-2 * l) / (r - l)) - 1
        self.normalization_matrix[2][1] = ((-2 * b) / (t - b)) - 1
        self.transformation_stack[-1] = self.normalization_matrix * \
                                        self.transformation_stack[-1]

    # get the viewing window
    def defineViewWindow(self, t, b, r, l):
        self.view_matrix[0][0] = ((r - l) / 2)
        self.view_matrix[1][1] = ((t - b) / 2)
        self.view_matrix[2][0] = ((r + l) / 2)
        self.view_matrix[2][1] = ((t + b) / 2)
        self.transformation_stack[-1] = self.view_matrix * \
                                        self.transformation_stack[-1]

    # push object to the stack
    def pushTransform(self):
        if not self.transformation_stack:
            self.transformation_stack.append(glm.mat4(1.0))
        else:
            self.transformation_stack.append(
                copy.deepcopy(self.transformation_stack[-1]))

    # pop from the stack
    def popTransform(self):
        self.transformation_stack.pop()

    # draw the projection of the 3D object
    def drawTrianglesC(self, vertex_pos, indices, r, g, b, outr=-1, outg=-1,
                       outb=-1):
        for ind in range(0, len(indices), 3):
            vertices = []
            for i in indices[ind: ind + 3]:
                x, y, z = vertex_pos[3 * i], vertex_pos[3 * i + 1], vertex_pos[
                    3 * i + 2]
                vertices.append(Vertex(x, y, z, r, g, b))

            for i in range(len(vertices)):
                original_vertex = glm.vec4(vertices[i].x, vertices[i].y,
                                           vertices[i].z, 1)

                projected_vertex = self.view_port * self.projection_transform * self.viewing_transform * \
                                   self.transformation_stack[
                                       -1] * original_vertex

                if projected_vertex.w != 0:
                    projected_vertex.x /= projected_vertex.w
                    projected_vertex.y /= projected_vertex.w
                    projected_vertex.z /= projected_vertex.w

                vertices[i].x = int(projected_vertex.x)
                vertices[i].y = int(projected_vertex.y)
                vertices[i].z = int(projected_vertex.z)

            self.rasterizeTriangle(vertices[0], vertices[1], vertices[2])

            # get vertices
            p0, p1, p2 = glm.vec3(vertices[0].x, vertices[0].y, vertices[0].z), \
                glm.vec3(vertices[1].x, vertices[1].y, vertices[1].z), \
                glm.vec3(vertices[2].x, vertices[2].y, vertices[2].z)

            E1, E2 = p1 - p0, p2 - p0

            # calculate normal vector for z-axis
            cross_product_x = E1[1] * E2[2] - E1[2] * E2[1]
            cross_product_y = E1[2] * E2[0] - E1[0] * E2[2]
            cross_product_z = E1[0] * E2[1] - E1[1] * E2[0]

            # skip rear-facing triangles
            if cross_product_z < 0:
                continue

            self.rasterizeLine(vertices[0].x, vertices[0].y, vertices[1].x,
                               vertices[1].y, outr, outg, outb)
            self.rasterizeLine(vertices[1].x, vertices[1].y, vertices[2].x,
                               vertices[2].y, outr, outg, outb)
            self.rasterizeLine(vertices[2].x, vertices[2].y, vertices[0].x,
                               vertices[0].y, outr, outg, outb)

    # draw wireframes for the object
    def drawTrianglesWireframe(self, vertex_pos, indices, r, g, b):
        for ind in range(0, len(indices), 3):
            vertices = []
            for i in indices[ind: ind + 3]:
                x, y, z = vertex_pos[3 * i], vertex_pos[3 * i + 1], vertex_pos[
                    3 * i + 2]
                vertices.append(Vertex(x, y, z, r, g, b))

            for i in range(len(vertices)):
                original_vertex = glm.vec3(vertices[i].x, vertices[i].y,
                                           vertices[i].z)

                transformed_vertex = self.view_matrix * self.normalization_matrix * self.model_matrix * original_vertex

                vertices[i].x = int(transformed_vertex.x)
                vertices[i].y = int(transformed_vertex.y)
                vertices[i].z = int(transformed_vertex.z)

            # get vertices
            p0, p1, p2 = glm.vec3(vertices[0].x, vertices[0].y, vertices[0].z), \
                glm.vec3(vertices[1].x, vertices[1].y, vertices[1].z), \
                glm.vec3(vertices[2].x, vertices[2].y, vertices[2].z)

            E1, E2 = p1 - p0, p2 - p0

            # calculate normal vector for z-axis
            cross_product_x = E1[1] * E2[2] - E1[2] * E2[1]
            cross_product_y = E1[2] * E2[0] - E1[0] * E2[2]
            cross_product_z = E1[0] * E2[1] - E1[1] * E2[0]

            # skip rear-facing triangles
            if cross_product_z < 0:
                continue

            self.rasterizeLine(vertices[0].x, vertices[0].y, vertices[1].x,
                               vertices[1].y, r, g, b)
            self.rasterizeLine(vertices[1].x, vertices[1].y, vertices[2].x,
                               vertices[2].y, r, g, b)
            self.rasterizeLine(vertices[2].x, vertices[2].y, vertices[0].x,
                               vertices[0].y, r, g, b)

    def setCamera(self, eye, lookAt, up):
        self.viewing_transform = glm.lookAtRH(eye, lookAt, up)
        self.eye = eye

    def setOrtho(self, l, r, b, t, n, f):
        self.projection_transform = glm.orthoRH_NO(l, r, b, t, n, f)

    def setFrustum(self, l, r, b, t, n, f):
        self.projection_transform = glm.frustumRH_NO(l, r, b, t, n, f)

    def setLight(self, pos, C):
        self.light_position = glm.vec3(pos[0], pos[1], pos[2])
        self.light_color = glm.vec3(C[0], C[1], C[2])

    def setAmbient(self, C):
        self.ambient_color = glm.vec3(C[0], C[1], C[2])

    def drawTrianglesPhong(self, vertex_pos, indices, normals, ocolor, scolor,
                           k, exponent, doGouraud):
        for ind in range(0, len(indices), 3):
            vertices = []

            for i in indices[ind: ind + 3]:
                x, y, z = vertex_pos[3 * i], vertex_pos[3 * i + 1], vertex_pos[
                    3 * i + 2]
                nx, ny, nz = normals[3 * i], vertex_pos[3 * i + 1], vertex_pos[
                    3 * i + 2]
                vertices.append(
                    Vertex(x, y, z, ocolor[0], ocolor[1], ocolor[2], nx, ny,
                           nz))

            for i in range(len(vertices)):
                original_vertex = glm.vec4(vertices[i].x, vertices[i].y,
                                           vertices[i].z, 1)

                projected_vertex = self.view_port * self.projection_transform * self.viewing_transform * \
                                   self.transformation_stack[
                                       -1] * original_vertex

                if projected_vertex.w != 0:
                    projected_vertex.x /= projected_vertex.w
                    projected_vertex.y /= projected_vertex.w
                    projected_vertex.z /= projected_vertex.w

                vertices[i].x = int(projected_vertex.x)
                vertices[i].y = int(projected_vertex.y)
                vertices[i].z = int(projected_vertex.z)

                # Calculate lighting using the Phong reflection model
                view_vector = glm.normalize(self.eye - glm.normalize(
                    glm.vec3(vertices[i].x, vertices[i].y, vertices[i].z)))

                light_dir = glm.normalize(self.light_position + glm.normalize(
                    glm.vec3(vertices[i].x, vertices[i].y, vertices[i].z)))

                vec = glm.normalize(
                    glm.vec4(vertices[i].x, vertices[i].y, vertices[i].z, 1))
                normal = glm.normalize(
                    glm.vec3(vertices[i].n0, vertices[i].n1, vertices[i].n2))
                new_normal = glm.normalize(
                    glm.transpose(glm.inverse(self.model_matrix)) * normal)

                light_vector = glm.normalize(
                    self.light_position - glm.vec3(vec[0], vec[1], vec[2]))
                reflect_vector = glm.normalize(
                    glm.reflect(-light_dir, new_normal))

                # ambient component
                ambient = ocolor * self.ambient_color
                cos_theta = glm.dot(new_normal, light_vector) if glm.dot(
                    new_normal, light_vector) > 0 else 0

                # diffuse component
                diffuse = (self.light_color * ocolor) * cos_theta
                cos_alpha = glm.dot(reflect_vector, view_vector) if glm.dot(
                    reflect_vector, view_vector) > 0 else 0

                # specular component
                specular = self.light_color * scolor * pow(cos_alpha, exponent)

                # Combine lighting components
                if doGouraud:
                    final_color = k[0] * ambient + k[1] * diffuse + k[
                        2] * specular

                vertices[i].r = final_color[0] * 255
                vertices[i].g = final_color[1] * 255
                vertices[i].b = final_color[2] * 255

                # Calculate light vectors at vertices
                L0 = glm.normalize(
                    self.light_position - glm.vec3(vertices[0].x,
                                                   vertices[0].y,
                                                   vertices[0].z))
                L1 = glm.normalize(
                    self.light_position - glm.vec3(vertices[1].x,
                                                   vertices[1].y,
                                                   vertices[1].z))
                L2 = glm.normalize(
                    self.light_position - glm.vec3(vertices[2].x,
                                                   vertices[2].y,
                                                   vertices[2].z))

                # Interpolate light vectors
                # interpolated_L = glm.normalize(self.lambda0 * L0 + self.lambda1 * L1 + self.lambda2 * L2)

            self.rasterizeTriangle(vertices[0], vertices[1], vertices[2])

    def drawTrianglesTextures(self, vertex_pos, indices, uvs, image):
        for ind in range(0, len(indices), 3):
            vertices = []

            for i in indices[ind: ind + 3]:
                x, y, z = vertex_pos[3 * i], vertex_pos[3 * i + 1], vertex_pos[
                    3 * i + 2]
                u, v = uvs[2 * i], uvs[2 * i + 1]
                # r, g, b = self.texture(u, v, image)
                vertices.append(Vertex(x, y, z, 1, 1, 1, 0, 0, 0, u, v))

            for i in range(len(vertices)):
                original_vertex = glm.vec4(vertices[i].x, vertices[i].y,
                                           vertices[i].z, 1)
                projected_vertex = self.view_port * self.projection_transform * self.viewing_transform * \
                                   self.transformation_stack[
                                       -1] * original_vertex

                if projected_vertex.w != 0:
                    projected_vertex.x /= projected_vertex.w
                    projected_vertex.y /= projected_vertex.w
                    projected_vertex.z /= projected_vertex.w

                vertices[i].x = int(projected_vertex.x)
                vertices[i].y = int(projected_vertex.y)
                vertices[i].z = int(projected_vertex.z)

            self.rasterizeTriangle(vertices[0], vertices[1], vertices[2], image)

    def drawTrianglesMyTextures(self, vertex_pos, indices, uvs):
        for ind in range(0, len(indices), 3):
            vertices = []

            for i in indices[ind: ind + 3]:
                x, y, z = vertex_pos[3 * i], vertex_pos[3 * i + 1], vertex_pos[
                    3 * i + 2]
                u, v = uvs[2 * i], uvs[2 * i + 1]
                vertices.append(Vertex(x, y, z, 1, 1, 1, 0, 0, 0, u, v))

            for i in range(len(vertices)):
                original_vertex = glm.vec4(vertices[i].x, vertices[i].y,
                                           vertices[i].z, 1)
                projected_vertex = self.view_port * self.projection_transform * self.viewing_transform * \
                                   self.transformation_stack[
                                       -1] * original_vertex

                if projected_vertex.w != 0:
                    projected_vertex.x /= projected_vertex.w
                    projected_vertex.y /= projected_vertex.w
                    projected_vertex.z /= projected_vertex.w

                vertices[i].x = int(projected_vertex.x)
                vertices[i].y = int(projected_vertex.y)
                vertices[i].z = int(projected_vertex.z)

            self.rasterizeTriangle(vertices[0], vertices[1], vertices[2], None)

    def keyboard(self, key):
        if key == '1':
            self.keypressed = 1
            self.go()
        if key == '2':
            self.keypressed = 2
            self.go()

    # go is called on every update of the window display loop
    # have your engine draw stuff in the window.
    def go(self):
        if self.keypressed == 1:
            # default scene
            self.default_action()

        if self.keypressed == 2:
            # add you own unique scene here
            self.win.clearFB(0, 0, 0)

            # push the window's framebuffer to the window
        self.win.applyFB()
