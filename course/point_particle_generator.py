import random
import glm
from particle import Particle


class PointParticleGenerator:
    def __init__(self, pos: glm.vec3, direction: glm.vec3):
        self._pos = pos
        self._direction = self.normalize(direction)

    def __call__(self):
        # Генерируем случайное отклонение для скорости
        offset = 0.3
        random_offset = [
            (random.uniform(-offset, offset)),  # небольшое отклонение по x
            (random.uniform(-offset, offset)),  # небольшое отклонение по y
            (random.uniform(-offset, offset))  # небольшое отклонение по z
        ]

        # Устанавливаем скорость как направление с небольшим отклонением
        velocity = self._direction + random_offset
        velocity = self.normalize(velocity)  # Нормализуем итоговый вектор скорости

        # Возвращаем частицу с позицией, скоростью и другими параметрами
        return Particle(self._pos, velocity * 2.0, [1.0, 0.0, 0.0, 1.0], 7.0, random.randint(7, 10))

    @staticmethod
    def normalize(vec: glm.vec3) -> glm.vec3:
        magnitude = sum(x ** 2 for x in vec.to_list()) ** 0.5
        return vec / magnitude if magnitude != 0 else glm.vec3(0.0, 0.0, 0.0)
