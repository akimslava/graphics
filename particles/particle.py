import glm


class Particle:
    def __init__(self, pos=None, vel=None, color=None, life=0.0):
        self.pos = pos if pos is not None else glm.vec3(0.0)
        self.vel = vel if vel is not None else glm.vec3(0.0)
        self.color = color if color is not None else glm.vec4(1.0)
        self.life = life

    def is_dead(self):
        return self.life <= 0.0

    def kill(self):
        self.life = 0.0
