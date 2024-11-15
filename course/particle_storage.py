from typing import List
from particle import Particle


class ParticleStorage:
    def __init__(self, amount: int):
        self._particles: List[Particle] = [Particle() for _ in range(amount)]
        self._death_particle_it = 0  # Указатель на первую "мертвую" частицу
        self._alive_particles = 0

    def alive_count(self) -> int:
        return self._alive_particles

    def is_full(self) -> bool:
        return self.alive_count() == len(self._particles)

    def get_alive_particles(self) -> List[Particle]:
        return self._particles[:self._alive_particles]

    def make_particle(self, new_particle: Particle):
        if self.is_full():
            raise RuntimeError("Storage is full!")

        self._particles[self._death_particle_it] = new_particle
        self._death_particle_it += 1
        self._alive_particles += 1

    def clear_dead_particles(self):
        # Очистка "мертвых" частиц
        i = 0
        while i < self._death_particle_it:
            if self._particles[i].is_dead():
                # Перемещаем мертвую частицу в конец "живых"
                self._death_particle_it -= 1
                self._particles[i], self._particles[self._death_particle_it] = self._particles[self._death_particle_it], \
                self._particles[i]
                self._alive_particles -= 1
            else:
                i += 1