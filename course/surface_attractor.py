import glm

from particle import Particle


class SurfaceAttractor:
    def __init__(self, pos, size, strength):
        self._pos = pos
        self._size = size
        self._strength = strength

    def __call__(self, particle: Particle, dt: float):
        # Half side length of the plane's square
        half_size = self._size / 2.0

        # Clamp particle position to the bounds of the square plane on X and Z
        nearest_x = max(-half_size, min(particle.pos.x, half_size))
        nearest_z = max(-half_size, min(particle.pos.z, half_size))

        # Vector pointing to the nearest point on the plane
        nearest_point_on_plane = glm.vec3(nearest_x, self._pos.y, nearest_z)
        direction_to_plane = nearest_point_on_plane - particle.pos

        # Calculate the attraction force based on the distance
        distance_to_plane = glm.length(direction_to_plane)

        if distance_to_plane > 0.0:
            # Calculate force direction and magnitude
            force_direction = glm.normalize(direction_to_plane)
            force_magnitude = self._strength / (distance_to_plane * distance_to_plane)
            force = force_magnitude * force_direction

            # Apply force to particle velocity
            particle.vel += force * dt
