from math import pi, sin, cos

import numpy as np
from OpenGL.GL import *


class Sphere:
    def __init__(self, radius=1.0):
        stack_count = 64
        sector_count = 64

        vertices = []
        indices_vector = []

        length_inv = 1.0 / radius

        sector_step = 2 * pi / sector_count
        stack_step = pi / stack_count

        for i in range(stack_count + 1):
            stack_angle = pi / 2 - i * stack_step
            xy = radius * cos(stack_angle)
            z = radius * sin(stack_angle)

            for j in range(sector_count + 1):
                sector_angle = j * sector_step

                x = xy * cos(sector_angle)
                y = xy * sin(sector_angle)

                nx = x * length_inv
                ny = y * length_inv
                nz = z * length_inv

                s = j / sector_count
                t = i / stack_count

                vertices.extend([x, y, z, nx, ny, nz, s, t])

        for i in range(stack_count):
            k1 = i * (sector_count + 1)
            k2 = k1 + sector_count + 1

            for j in range(sector_count):
                if i != 0:
                    indices_vector.extend([k1, k2, k1 + 1])

                if i != (stack_count - 1):
                    indices_vector.extend([k1 + 1, k2, k2 + 1])

                k1 += 1
                k2 += 1

        self._vertices_count = len(vertices) // 8
        self._ind_count = len(indices_vector)

        vertices = np.array(vertices, dtype=np.float32)
        indices_vector = np.array(indices_vector, dtype=np.uint32)

        self.VAO = glGenVertexArrays(1)
        self.VBO = glGenBuffers(1)
        self.IBO = glGenBuffers(1)

        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        glBindVertexArray(self.VAO)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8 * vertices.itemsize, ctypes.c_void_p(0))

        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 8 * vertices.itemsize, ctypes.c_void_p(3 * vertices.itemsize))

        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 8 * vertices.itemsize, ctypes.c_void_p(6 * vertices.itemsize))

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.IBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices_vector.nbytes, indices_vector, GL_STATIC_DRAW)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def render(self):
        glBindVertexArray(self.VAO)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.IBO)
        glDrawElements(GL_TRIANGLE_STRIP, self._ind_count, GL_UNSIGNED_INT, None)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

