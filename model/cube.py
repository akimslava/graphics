from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np


class Cube:
    def __init__(self):
        # Определение вершин куба
        vertices = np.array([
            # back face
            -1.0, 0.0, -1.0, 0.0, 0.0, -1.0, 0.0, 0.0, # bottom-left
            1.0, 2.0, -1.0, 0.0, 0.0, -1.0, 1.0, 1.0,  # top-right
            1.0, 0.0, -1.0, 0.0, 0.0, -1.0, 1.0, 0.0,  # bottom-right
            1.0, 2.0, -1.0, 0.0, 0.0, -1.0, 1.0, 1.0,  # top-right
            -1.0, 0.0, -1.0, 0.0, 0.0, -1.0, 0.0, 0.0, # bottom-left
            -1.0, 2.0, -1.0, 0.0, 0.0, -1.0, 0.0, 1.0, # top-left
            # front face
            -1.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, # bottom-left
            1.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0,  # bottom-right
            1.0, 2.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0,  # top-right
            1.0, 2.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0,  # top-right
            -1.0, 2.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0, # top-left
            -1.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, # bottom-left
            # left face
            -1.0, 2.0, 1.0, -1.0, 0.0, 0.0, 1.0, 0.0,  # top-right
            -1.0, 2.0, -1.0, -1.0, 0.0, 0.0, 1.0, 1.0, # top-left
            -1.0, 0.0, -1.0, -1.0, 0.0, 0.0, 0.0, 1.0, # bottom-left
            -1.0, 0.0, -1.0, -1.0, 0.0, 0.0, 0.0, 1.0, # bottom-left
            -1.0, 0.0, 1.0, -1.0, 0.0, 0.0, 0.0, 0.0,  # bottom-right
            -1.0, 2.0, 1.0, -1.0, 0.0, 0.0, 1.0, 0.0,  # top-right
                                                               # right face
            1.0, 2.0, 1.0, 1.0, 0.0, 0.0, 1.0, 0.0,    # top-left
            1.0, 0.0, -1.0, 1.0, 0.0, 0.0, 0.0, 1.0,   # bottom-right
            1.0, 2.0, -1.0, 1.0, 0.0, 0.0, 1.0, 1.0,   # top-right
            1.0, 0.0, -1.0, 1.0, 0.0, 0.0, 0.0, 1.0,   # bottom-right
            1.0, 2.0, 1.0, 1.0, 0.0, 0.0, 1.0, 0.0,    # top-left
            1.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0,    # bottom-left
            # bottom face
            -1.0, 0.0, -1.0, 0.0, -1.0, 0.0, 0.0, 1.0, # top-right
            1.0, 0.0, -1.0, 0.0, -1.0, 0.0, 1.0, 1.0,  # top-left
            1.0, 0.0, 1.0, 0.0, -1.0, 0.0, 1.0, 0.0,   # bottom-left
            1.0, 0.0, 1.0, 0.0, -1.0, 0.0, 1.0, 0.0,   # bottom-left
            -1.0, 0.0, 1.0, 0.0, -1.0, 0.0, 0.0, 0.0,  # bottom-right
            -1.0, 0.0, -1.0, 0.0, -1.0, 0.0, 0.0, 1.0, # top-right
            # top face
            -1.0, 2.0, -1.0, 0.0, 1.0, 0.0, 0.0, 1.0, # top-left
            1.0, 2.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0,   # bottom-right
            1.0, 2.0, -1.0, 0.0, 1.0, 0.0, 1.0, 1.0,  # top-right
            1.0, 2.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0,   # bottom-right
            -1.0, 2.0, -1.0, 0.0, 1.0, 0.0, 0.0, 1.0, # top-left
            -1.0, 2.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0   # bottom-left
        ], dtype=np.float32)

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
