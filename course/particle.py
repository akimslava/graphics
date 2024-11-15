import glm
from collections import deque


class Particle:
    def __init__(self, pos=None, vel=None, color=None, life=0.0, trace_length=1):
        self.pos = pos if pos is not None else glm.vec3(0.0)
        self.vel = vel if vel is not None else glm.vec3(0.0)
        self.color = color if color is not None else glm.vec4(1.0)
        self.life = life
        self.old_pos = deque([self.pos] * (trace_length - 1))

    def set_trace_length(self, trace_length):
        # Initialize old_pos with the current position `pos`, `trace_length - 1` times
        self.old_pos = deque([self.pos] * (trace_length - 1))

    def is_dead(self):
        return self.life <= 0.0

    def kill(self):
        self.life = 0.0


class LifeComparator:
    def __call__(self, p1, p2):
        return p1.life < p2.life


class DeadPredicate:
    def __call__(self, p):
        return p.is_dead()