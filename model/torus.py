import math

import glfw
import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *


class Torus:
    def __init__(self, radius_in, radius_out):
        self.radius_in = radius_in
        self.radius_out = radius_out
        self.vertices: np.ndarray = np.array(0)
        self.VAO = None
        self.VBO = None
        self._vertices_count = 0
        self.create_vertices()

    def create_vertices(self):
        n_r = 64
        nr = 64

        vertices = []

        du = 2 * np.pi / n_r
        dv = 2 * np.pi / nr

        for i in range(n_r):
            u = i * du
            for j in range(nr + 1):
                v = (j % nr) * dv

                for k in range(2):
                    uu = u + k * du
                    _x = (self.radius_out + self.radius_in * math.cos(v)) * math.cos(uu)
                    _y = (self.radius_out + self.radius_in * math.cos(v)) * math.sin(uu)
                    _z = self.radius_in * math.sin(v)

                    nx = math.cos(v) * math.cos(uu)
                    ny = math.cos(v) * math.sin(uu)
                    nz = math.sin(v)

                    tx = uu / (2 * np.pi)
                    ty = v / (2 * np.pi)

                    vertices.extend([_x, _y, _z, nx, ny, nz, tx, ty])

                v += dv

        self._vertices_count = len(vertices) // 8
        self.vertices = np.array(vertices, dtype=np.float32)

        self.setup_buffers()

    def setup_buffers(self):
        self.VAO = glGenVertexArrays(1)
        self.VBO = glGenBuffers(1)

        glBindVertexArray(self.VAO)

        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8 * 4, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 8 * 4, ctypes.c_void_p(3 * 4))
        glEnableVertexAttribArray(1)

        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 8 * 4, ctypes.c_void_p(6 * 4))
        glEnableVertexAttribArray(2)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def render(self):
        glBindVertexArray(self.VAO)
        glDrawArrays(GL_TRIANGLE_STRIP, 0, self._vertices_count)
        glBindVertexArray(0)


def main():
    if not glfw.init():
        return

    window = glfw.create_window(800, 600, "Torus Example", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    torus = Torus(0.2, 0.5)

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        torus.render()

        glfw.swap_buffers(window)

        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()