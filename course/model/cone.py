import math

import numpy as np
from OpenGL.GL import *


class Cone:
    def __init__(self, radius, height):
        sides = 128
        vertices = []

        theta = 2.0 * math.pi / sides
        c = math.cos(theta)
        s = math.sin(theta)
        
        x2 = radius
        z2 = 0.0
        
        for i in range(sides + 1):
            tx = float(i) / sides
            
            nf = 1.0 / math.sqrt(x2 * x2 + z2 * z2)
            xn = x2 * nf
            zn = z2 * nf
            
            vertices.extend([x2, 0.0, z2, xn, 0.0, zn, tx, 0.0])
            vertices.extend([0.0, height, 0.0, 0.0, 1.0, 0.0, tx, 1.0])

            x3 = x2
            x2 = c * x2 - s * z2
            z2 = s * x3 + c * z2

        self._vertices_count = len(vertices) // 8
        vertices = np.array(vertices, dtype='float32')

        self.VAO = glGenVertexArrays(1)
        self.VBO = glGenBuffers(1)
        
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        glBindVertexArray(self.VAO)
        stride = 8 * ctypes.sizeof(ctypes.c_float)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, None)
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(3 * ctypes.sizeof(ctypes.c_float)))
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(6 * ctypes.sizeof(ctypes.c_float)))
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def render(self):
        glBindVertexArray(self.VAO)
        glDrawArrays(GL_TRIANGLE_STRIP, 0, self._vertices_count)
        glBindVertexArray(0)
