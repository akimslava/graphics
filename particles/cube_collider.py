import numpy as np


def line_plane_intersection(ray, ray_origin, normal, coord):
    d = np.dot(normal, coord)

    if np.dot(normal, ray) == 0:
        return None  # Нет пересечения, линия параллельна плоскости

    # Вычисление значения X для направленного луча, пересекающего плоскость
    x = (d - np.dot(normal, ray_origin)) / np.dot(normal, ray)
    return ray_origin + (ray / np.linalg.norm(ray)) * x


class CubeCollider:
    def __init__(self, center_pos, cube):
        self.planes = cube.planes
        self._center_pos = center_pos
        self._length = cube.length

    def __call__(self, particle, dt):
        half_size = self._length / 2.0

        # Расчет предполагаемой новой позиции
        next_pos = particle.pos + particle.vel * dt

        dx = np.array([1.0, 0.0, 0.0])
        dy = np.array([0.0, 1.0, 0.0])
        dz = np.array([0.0, 0.0, 1.0])

        d = next_pos - self._center_pos
        inside = (abs(np.dot(d, dx)) <= half_size and
                  abs(np.dot(d, dy)) <= half_size and
                  abs(np.dot(d, dz)) <= half_size)

        if inside:
            plane_normal = None
            min_dist = float('inf')

            for plane in self.planes:
                res = line_plane_intersection(next_pos - particle.pos, particle.pos, plane.normal,
                                              plane.pos + self._center_pos)

                if res is not None:
                    dist = np.linalg.norm(res - particle.pos)
                    if dist < min_dist:
                        min_dist = dist
                        plane_normal = plane.normal

            if plane_normal is not None:
                # Отражение скорости вручную
                particle.vel = particle.vel - 2 * np.dot(particle.vel, plane_normal) * plane_normal

                # Обновляем позицию частицы на следующую
                particle.pos = next_pos
