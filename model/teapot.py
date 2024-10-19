import glm
import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *


class Teapot:
    def __init__(self, obj_path):
        self.VAO = glGenVertexArrays(1)
        self.VBO = glGenBuffers(1)
        vertices = self._load_model(obj_path)
        self._vertices_count = len(vertices) // 8

        glBindVertexArray(self.VAO)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8 * np.dtype(np.float32).itemsize, ctypes.c_void_p(0))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 8 * np.dtype(np.float32).itemsize, ctypes.c_void_p(3 * np.dtype(np.float32).itemsize))
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 8 * np.dtype(np.float32).itemsize, ctypes.c_void_p(6 * np.dtype(np.float32).itemsize))
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def render(self):
        glBindVertexArray(self.VAO)
        glDrawArrays(GL_TRIANGLES, 0, self._vertices_count)
        glBindVertexArray(0)

    @staticmethod
    def _load_model(obj_path):
        vertices = []

        temp_vertices = []
        temp_uvs = []
        temp_normals = []
        vertex_indices = []
        uv_indices = []
        normal_indices = []

        with open(obj_path) as file:
            for line in file:
                if line.startswith('v '):
                    parts = line.strip().split()[1:]
                    vertex = glm.vec3(float(parts[0]), float(parts[1]), float(parts[2]))
                    temp_vertices.append(vertex)
                elif line.startswith('vt '):
                    parts = line.strip().split()[1:]
                    uv = glm.vec2(float(parts[0]), -float(parts[1]))  # Invert the y coordinate
                    temp_uvs.append(uv)
                elif line.startswith('vn '):
                    parts = line.strip().split()[1:]
                    normal = glm.vec3(float(parts[0]), float(parts[1]), float(parts[2]))
                    temp_normals.append(normal)
                elif line.startswith('f '):
                    face = line.strip().split()[1:]
                    for vertex in face:
                        indices = vertex.split('/')
                        vertex_indices.append(int(indices[0]) - 1)
                        uv_indices.append(int(indices[1]) - 1)
                        normal_indices.append(int(indices[2]) - 1)

        for i in range(len(vertex_indices)):
            vertex = temp_vertices[vertex_indices[i]]
            uv = temp_uvs[uv_indices[i]]
            normal = temp_normals[normal_indices[i]]

            vertices.extend([vertex.x, vertex.y, vertex.z, normal.x, normal.y, normal.z, uv.x, uv.y])

        return np.array(vertices, dtype=np.float32)
