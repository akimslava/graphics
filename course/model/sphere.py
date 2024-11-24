from OpenGL.GL import *
from math import pi, sin, cos
import numpy as np


class Sphere:
    def __init__(self, radius=1.0):
        stackCount = 64
        sectorCount = 64

        vertices = []
        indicesVector = []

        lengthInv = 1.0 / radius

        sectorStep = 2 * pi / sectorCount
        stackStep = pi / stackCount

        # Генерация вершин
        for i in range(stackCount + 1):
            stackAngle = pi / 2 - i * stackStep  # от pi/2 до -pi/2
            xy = radius * cos(stackAngle)  # r * cos(u)
            z = radius * sin(stackAngle)  # r * sin(u)

            for j in range(sectorCount + 1):
                sectorAngle = j * sectorStep  # от 0 до 2pi

                # Позиции вершин (x, y, z)
                x = xy * cos(sectorAngle)  # r * cos(u) * cos(v)
                y = xy * sin(sectorAngle)  # r * cos(u) * sin(v)

                # Нормали (nx, ny, nz)
                nx = x * lengthInv
                ny = y * lengthInv
                nz = z * lengthInv

                # Текстурные координаты (s, t)
                s = j / sectorCount
                t = i / stackCount

                vertices.extend([x, y, z, nx, ny, nz, s, t])

        # Генерация индексов
        for i in range(stackCount):
            k1 = i * (sectorCount + 1)
            k2 = k1 + sectorCount + 1

            for j in range(sectorCount):
                if i != 0:
                    indicesVector.extend([k1, k2, k1 + 1])

                if i != (stackCount - 1):
                    indicesVector.extend([k1 + 1, k2, k2 + 1])

                k1 += 1
                k2 += 1

        self._vertices_count = len(vertices) // 8
        self._ind_count = len(indicesVector)

        vertices = np.array(vertices, dtype=np.float32)
        indicesVector = np.array(indicesVector, dtype=np.uint32)

        # Генерация VAO, VBO, IBO
        self.VAO = glGenVertexArrays(1)
        self.VBO = glGenBuffers(1)
        self.IBO = glGenBuffers(1)

        # Привязка VBO
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        # Привязка VAO
        glBindVertexArray(self.VAO)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8 * vertices.itemsize, ctypes.c_void_p(0))

        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 8 * vertices.itemsize, ctypes.c_void_p(3 * vertices.itemsize))

        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 8 * vertices.itemsize, ctypes.c_void_p(6 * vertices.itemsize))

        # Привязка IBO
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.IBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indicesVector.nbytes, indicesVector, GL_STATIC_DRAW)

        # Отвязка VAO и VBO
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def render(self):
        glBindVertexArray(self.VAO)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.IBO)
        glDrawElements(GL_TRIANGLE_STRIP, self._ind_count, GL_UNSIGNED_INT, None)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

