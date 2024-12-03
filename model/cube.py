import glm

from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np

from model.plane import Plane


class Cube:
    def __init__(self, length):
        self.length = length

        half_length = length / 2.0
        # Определение вершин куба
        vertices = np.array([
            # back face
            -half_length, -half_length, -half_length, 0.0, 0.0, -1.0, 0.0, 0.0,  # bottom-left
            half_length, half_length, -half_length, 0.0, 0.0, -1.0, 1.0, 1.0,  # top-right
            half_length, -half_length, -half_length, 0.0, 0.0, -1.0, 1.0, 0.0,  # bottom-right
            half_length, half_length, -half_length, 0.0, 0.0, -1.0, 1.0, 1.0,  # top-right
            -half_length, -half_length, -half_length, 0.0, 0.0, -1.0, 0.0, 0.0,  # bottom-left
            -half_length, half_length, -half_length, 0.0, 0.0, -1.0, 0.0, 1.0,  # top-left

            # front face
            -half_length, -half_length, half_length, 0.0, 0.0, 1.0, 0.0, 0.0,  # bottom-left
            half_length, half_length, half_length, 0.0, 0.0, 1.0, 1.0, 1.0,  # bottom-right
            half_length, -half_length, half_length, 0.0, 0.0, 1.0, 1.0, 0.0,  # top-right
            half_length, half_length, half_length, 0.0, 0.0, 1.0, 1.0, 1.0,  # top-right
            -half_length, -half_length, half_length, 0.0, 0.0, 1.0, 0.0, 0.0,  # top-left
            -half_length, half_length, half_length, 0.0, 0.0, 1.0, 0.0, 1.0,  # bottom-left

            # left face
            -half_length, half_length, half_length, -1.0, 0.0, 0.0, 1.0, 0.0,  # top-right
            -half_length, -half_length, -half_length, -1.0, 0.0, 0.0, 0.0, 1.0,  # top-left
            -half_length, half_length, -half_length, -1.0, 0.0, 0.0, 1.0, 1.0,  # bottom-left
            -half_length, -half_length, -half_length, -1.0, 0.0, 0.0, 0.0, 1.0,  # bottom-left
            -half_length, half_length, half_length, -1.0, 0.0, 0.0, 1.0, 0.0,  # bottom-right
            -half_length, -half_length, half_length, -1.0, 0.0, 0.0, 0.0, 0.0,  # top-right

            # right face
            half_length, half_length, half_length, 1.0, 0.0, 0.0, 1.0, 0.0,  # top-left
            half_length, -half_length, -half_length, 1.0, 0.0, 0.0, 0.0, 1.0,  # bottom-right
            half_length, half_length, -half_length, 1.0, 0.0, 0.0, 1.0, 1.0,  # top-right
            half_length, -half_length, -half_length, 1.0, 0.0, 0.0, 0.0, 1.0,  # bottom-right
            half_length, half_length, half_length, 1.0, 0.0, 0.0, 1.0, 0.0,  # top-left
            half_length, -half_length, half_length, 1.0, 0.0, 0.0, 0.0, 0.0,  # bottom-left

            # bottom face
            -half_length, -half_length, -half_length, 0.0, -1.0, 0.0, 0.0, 1.0,  # top-right
            half_length, -half_length, -half_length, 0.0, -1.0, 0.0, 1.0, 1.0,  # top-left
            half_length, -half_length, half_length, 0.0, -1.0, 0.0, 1.0, 0.0,  # bottom-left
            half_length, -half_length, half_length, 0.0, -1.0, 0.0, 1.0, 0.0,  # bottom-left
            -half_length, -half_length, half_length, 0.0, -1.0, 0.0, 0.0, 0.0,  # bottom-right
            -half_length, -half_length, -half_length, 0.0, -1.0, 0.0, 0.0, 1.0,  # top-right

            # top face
            -half_length, half_length, -half_length, 0.0, 1.0, 0.0, 0.0, 1.0,  # top-left
            half_length, half_length, half_length, 0.0, 1.0, 0.0, 1.0, 0.0,  # bottom-right
            half_length, half_length, -half_length, 0.0, 1.0, 0.0, 1.0, 1.0,  # top-right
            half_length, half_length, half_length, 0.0, 1.0, 0.0, 1.0, 0.0,  # bottom-right
            -half_length, half_length, -half_length, 0.0, 1.0, 0.0, 0.0, 1.0,  # top-left
            -half_length, half_length, half_length, 0.0, 1.0, 0.0, 0.0, 0.0  # bottom-left
        ], dtype=np.float32)

        self.planes = np.array([
            Plane(glm.vec3(0.0, 0.0, -1.0), glm.vec3((length / 2.0), -(length / 2.0), -(length / 2.0))), # back face
            Plane(glm.vec3(0.0, 0.0, 1.0), glm.vec3((length / 2.0), (length / 2.0), (length / 2.0))),    # front face
            Plane(glm.vec3(-1.0, 0.0, 0.0), glm.vec3(-(length / 2.0), (length / 2.0), -(length / 2.0))), # left face
            Plane(glm.vec3(1.0, 0.0, 0.0), glm.vec3((length / 2.0), (length / 2.0), -(length / 2.0))),   # right face
            Plane(glm.vec3(0.0, -1.0, 0.0), glm.vec3((length / 2.0), -(length / 2.0), (length / 2.0))),  # bottom face
            Plane(glm.vec3(0.0, 1.0, 0.0), glm.vec3((length / 2.0), (length / 2.0), -(length / 2.0)))    # top face
        ])

        # Генерация VAO и VBO
        self.VAO = glGenVertexArrays(1)
        self.VBO = glGenBuffers(1)

        # Связывание буфера
        glBindVertexArray(self.VAO)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        # Настройка атрибутов вершин
        glEnableVertexAttribArray(0)  # позиция
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8 * vertices.itemsize, ctypes.c_void_p(0))

        glEnableVertexAttribArray(1)  # нормали
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 8 * vertices.itemsize, ctypes.c_void_p(3 * vertices.itemsize))

        glEnableVertexAttribArray(2)  # текстурные координаты
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 8 * vertices.itemsize, ctypes.c_void_p(6 * vertices.itemsize))

        # Отвязываем буфер
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def render(self):
        glBindVertexArray(self.VAO)
        glDrawArrays(GL_TRIANGLES, 0, 36)
        glBindVertexArray(0)
