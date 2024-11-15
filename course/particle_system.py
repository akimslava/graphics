from OpenGL.GL import *
import numpy as np
from shader import Shader  # Assuming Shader class is defined elsewhere
from particle_storage import ParticleStorage


class ParticleSystem:
    def __init__(self, shader: Shader, amount: int, gen):
        self._particles = ParticleStorage(amount)  # A container for particles
        self._amount = amount
        self._shader_ptr = shader
        self._gen = gen

        # Create particle vertex buffer (one-point)
        particle_quad = np.array([
            0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0,
            1.0, 0.0, 0.0, 230.0 / 255.0, 244.0 / 255.0, 184.0 / 255, 0.3
        ], dtype=np.float32)

        self._VAO = glGenVertexArrays(1)
        VBO = glGenBuffers(1)

        glBindVertexArray(self._VAO)
        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBufferData(GL_ARRAY_BUFFER, particle_quad.nbytes, particle_quad, GL_STATIC_DRAW)

        # Set up vertex attributes
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 7 * particle_quad.itemsize, ctypes.c_void_p(0))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 4, GL_FLOAT, GL_FALSE, 7 * particle_quad.itemsize,
                              ctypes.c_void_p(3 * particle_quad.itemsize))

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def __del__(self):
        # Destructor for cleanup, if needed
        pass

    def render(self):
        glBlendFunc(GL_SRC_ALPHA, GL_ONE)

        for particle in self._particles.get_alive_particles():
            self._shader_ptr.set_vec3("old_pos", particle.old_pos.pop())  # Assuming old_pos is a list or queue

            self._shader_ptr.set_vec3("offset", particle.pos)
            self._shader_ptr.set_float("alpha", min(particle.life / 4.0, 1.0))

            glEnable(GL_LINE_SMOOTH)
            glBindVertexArray(self._VAO)
            glDrawArrays(GL_LINES, 0, 2)
            glBindVertexArray(0)

        # Reset to default blending mode
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def update(self, dt: float, new_particles: int, functor):
        self._makeNewParticles(new_particles)  # Добавляем новые частицы

        # Обновляем все "живые" частицы
        for particle in self._particles.get_alive_particles():
            particle.old_pos.appendleft(particle.pos)  # Сохраняем старую позицию
            particle.life -= dt  # Уменьшаем "жизнь" частицы

            # Применяем переданный functor для обновления состояния частицы
            functor(particle, dt)

            # Обновляем позицию частицы
            particle.pos = particle.pos + particle.vel * dt

        # Удаляем "мертвые" частицы
        self._particles.clear_dead_particles()

    def _makeNewParticles(self, count: int):
        for _ in range(count):
            if not self._particles.is_full():
                self._particles.make_particle(self._gen())

    def aliveCount(self) -> int:
        return self._particles.alive_count()
