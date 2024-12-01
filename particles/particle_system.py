import numpy as np
from OpenGL.GL import *

from particles.cone_gen import MAX_LIFE
from particles.particle_storage import ParticleStorage
from utils.shader import Shader

MIN_SIZE = 3

class ParticleSystem:
    def __init__(self, shader: Shader, amount: int, gen):
        self._particles = ParticleStorage(amount)
        self._amount = amount
        self._shader_ptr = shader
        self._gen = gen

        particle_quad = np.array([
            0.0, 0.0, 0.0, 128.0 / 255.0, 0.0, 128.0 / 255.0, 1.0,
        ], dtype=np.float32)

        self._VAO = glGenVertexArrays(1)
        VBO = glGenBuffers(1)

        glBindVertexArray(self._VAO)
        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBufferData(GL_ARRAY_BUFFER, particle_quad.nbytes, particle_quad, GL_STATIC_DRAW)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 7 * particle_quad.itemsize, ctypes.c_void_p(0))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 4, GL_FLOAT, GL_FALSE, 7 * particle_quad.itemsize,
                              ctypes.c_void_p(3 * particle_quad.itemsize))

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def render(self):
        glBlendFunc(GL_SRC_ALPHA, GL_ONE)

        for particle in self._particles.get_alive_particles():

            self._shader_ptr.set_vec3("offset", particle.pos)
            self._shader_ptr.set_float("alpha", min(particle.life / MAX_LIFE, 1.0))

            glPointSize(MAX_LIFE + 1 - particle.life + MIN_SIZE)
            glBindVertexArray(self._VAO)
            glDrawArrays(GL_POINTS, 0, 1)
            glBindVertexArray(0)

        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def update(self, dt: float, new_particles: int, functor):
        self._make_new_particles(new_particles)

        for particle in self._particles.get_alive_particles():
            particle.life -= dt

            functor(particle, dt)

            particle.pos = particle.pos + particle.vel * dt

        self._particles.clear_dead_particles()

    def _make_new_particles(self, count: int):
        for _ in range(count):
            if not self._particles.is_full():
                self._particles.make_particle(self._gen())

    def alive_count(self) -> int:
        return self._particles.alive_count()
