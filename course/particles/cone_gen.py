import glm
import numpy as np

from course.particles.particle import Particle

MAX_LIFE = 7.0

class ConeParticleGenerator:
    def __init__(self, center_pos, height, radius):
        self._center_pos = center_pos
        self._height = height
        self._radius = radius

    @classmethod
    def from_cone(cls, cone):
        return cls(cone.model_view().get_pos(), cone.get_height(), cone.get_radius())

    def __call__(self):
        theta = np.random.uniform(0, 2 * np.pi)
        y = np.random.uniform(0, self._height)

        r_current = self._radius * (self._height - y) / self._height
        x = r_current * np.cos(theta)
        z = r_current * np.sin(theta)

        normal_x = np.cos(theta)
        normal_z = np.sin(theta)
        normal_y = self._radius / self._height
        normal = np.array([normal_x, normal_y, normal_z])

        normalized_velocity = normal / np.linalg.norm(normal)

        return Particle(
            pos=self._center_pos + glm.vec3(x, y, z),
            vel=glm.vec3(*normalized_velocity),
            color=[1.0, 0.0, 0.0, 1.0],
            life=MAX_LIFE
        )
