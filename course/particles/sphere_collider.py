import numpy as np

class SphereCollider:
    def __init__(self, center_pos, radius):
        self._center_pos = center_pos
        self._radius = radius

    @classmethod
    def from_sphere(cls, sphere):
        """Alternative constructor using a sphere object."""
        return cls(sphere.model_view().get_pos(), sphere.get_radius())

    def __call__(self, particle, dt):
        next_pos = particle.pos + particle.vel * dt

        # Вычисление расстояния между частицей и центром сферы
        distance = np.linalg.norm(next_pos - self._center_pos)

        if distance <= self._radius:
            # Отражение скорости
            normal = (next_pos - self._center_pos) / distance
            particle.vel = particle.vel - 2 * np.dot(particle.vel, normal) * normal

            # Возвращение частицы в последнее безопасное положение
            particle.pos = next_pos
