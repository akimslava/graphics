import glm
import numpy as np

from particles.particle import Particle

MAX_LIFE = 7.0

class PlaneParticleGenerator:
    def __init__(self, center_pos, width, height, rotation_matrix=None):
        self._center_pos = center_pos
        self._width = width
        self._height = height
        self._rotation_matrix = rotation_matrix if rotation_matrix is not None else glm.mat4(1.0)

        # Извлекаем нормаль из матрицы поворота
        self._normal = glm.vec3(0.0, 1.0, 0.0)  # Изначальная нормаль для горизонтальной плоскости
        self._normal = glm.vec3(self._rotation_matrix * glm.vec4(self._normal, 0.0))  # Применяем матрицу поворота

        # Вектор нормали и D для уравнения плоскости
        self._A, self._B, self._C = self._normal.x, self._normal.y, self._normal.z
        self._D = glm.dot(self._normal, glm.vec3(self._center_pos.x, self._center_pos.y, self._center_pos.z))

    @classmethod
    def from_plane(cls, plane):
        # Получаем матрицу поворота для плоскости
        return cls(plane.model_view().get_pos(), plane.get_width(), plane.get_height(), plane.get_rotation_matrix())

    def __call__(self):
        # Случайным образом выбираем координаты (x, z) на плоскости
        x = np.random.uniform(-self._width / 2, self._width / 2)
        z = np.random.uniform(-self._height / 2, self._height / 2)

        # Вычисляем y для точки на плоскости, используя уравнение плоскости
        if self._B != 0:  # Чтобы избежать деления на ноль
            y = (self._D - self._A * x - self._C * z) / self._B
        else:
            y = self._center_pos.y  # В случае горизонтальной плоскости

        # Позиция точки на поверхности
        position_on_plane = self._center_pos + glm.vec3(x, y - self._center_pos.y, z)

        # Генерация случайной скорости частиц, направленной по нормали плоскости
        normalized_velocity = self._normal / glm.length(self._normal)

        return Particle(
            pos=position_on_plane,  # Позиция на поверхности
            vel=glm.vec3(*normalized_velocity),  # Направление скорости по нормали
            color=[1.0, 0.0, 0.0, 1.0],
            life=MAX_LIFE
        )
