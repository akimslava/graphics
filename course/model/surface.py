import numpy as np
from OpenGL.GL import *


class Surface:
    def __init__(self, size: float):
        self._size = size

        plane_vertices = np.array([
            size, 0.0, size, 0.0, 1.0, 0.0, size, 0.0,
            -size, 0.0, size, 0.0, 1.0, 0.0, 0.0, 0.0,
            -size, 0.0, -size, 0.0, 1.0, 0.0, 0.0, size,

            size, 0.0, size, 0.0, 1.0, 0.0, size, 0.0,
            -size, 0.0, -size, 0.0, 1.0, 0.0, 0.0, size,
            size, 0.0, -size, 0.0, 1.0, 0.0, size, size
        ], dtype=np.float32)

        self.VAO = glGenVertexArrays(1)
        self.VBO = glGenBuffers(1)

        glBindVertexArray(self.VAO)

        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, plane_vertices.nbytes, plane_vertices, GL_STATIC_DRAW)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8 * plane_vertices.itemsize, ctypes.c_void_p(0))

        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 8 * plane_vertices.itemsize,
                              ctypes.c_void_p(3 * plane_vertices.itemsize))

        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 8 * plane_vertices.itemsize,
                              ctypes.c_void_p(6 * plane_vertices.itemsize))

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def render(self):
        glBindVertexArray(self.VAO)
        glDrawArrays(GL_TRIANGLES, 0, 6)
        glBindVertexArray(0)
