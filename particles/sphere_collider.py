import numpy as np

class SphereCollider:
    def __init__(self, center_pos, radius):
        self._center_pos = center_pos
        self._radius = radius

    def __call__(self, particle, dt):
        next_pos = particle.pos + particle.vel * dt
        distance = np.linalg.norm(next_pos - self._center_pos)

        if distance <= self._radius:
            normal = (next_pos - self._center_pos) / distance
            particle.vel = particle.vel - 2 * np.dot(particle.vel, normal) * normal

            particle.pos = next_pos
